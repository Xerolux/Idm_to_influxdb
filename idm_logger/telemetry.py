# Xerolux 2026
# SPDX-License-Identifier: MIT
import os
import time
import logging
import requests
import json
import threading
import base64
import hmac
import hashlib
from cryptography.fernet import Fernet
from datetime import datetime
from .config import config
from .update_manager import get_current_version

logger = logging.getLogger(__name__)

# Default encryption key for community models (shared public key)
# In a real scenario, this might be rotated or fetched securely.
DEFAULT_ENCRYPTION_KEY = b"gR6xZ9jK3q2L5n8P7s4v1t0wY_mH-cJdKbNxVfZlQqA="

# Service URLs
ML_SERVICE_UPLOAD_URL = os.environ.get(
    "ML_SERVICE_UPLOAD_URL", "http://idm-ml-service:8080/model/upload"
)


class TelemetryManager:
    def __init__(self):
        self.running = False
        self.thread = None
        self.lock = threading.Lock()

        # Rate limiting state
        self.manual_downloads_today = 0
        self.last_manual_download = 0

        # Load state from config
        self._load_state()

    def _load_state(self):
        telemetry_config = config.get("telemetry", {})
        self.manual_downloads_today = telemetry_config.get("manual_downloads_today", 0)
        self.last_manual_download = telemetry_config.get("last_manual_download", 0)

        # Reset counter if it's a new day
        last_date = datetime.fromtimestamp(self.last_manual_download).date()
        if last_date < datetime.now().date():
            self.manual_downloads_today = 0
            self._save_state()

    def _save_state(self):
        config.set("telemetry.manual_downloads_today", self.manual_downloads_today)
        config.set("telemetry.last_manual_download", self.last_manual_download)
        config.save()

    def start(self, scheduler=None):
        if self.running:
            return

        self.running = True

        if scheduler:
            try:
                # Schedule jobs using APScheduler
                # Run submission every 24 hours (e.g., at 02:00)
                # Check if job exists to avoid duplicates if re-added?
                # APScheduler replace_existing=True usually handles it if id matches.

                scheduler.add_job(
                    func=self.submit_data_job,
                    trigger="cron",
                    hour=2,
                    minute=0,
                    id="telemetry_submit",
                    replace_existing=True,
                )

                # Run model check every 24 hours (e.g., at 04:00)
                scheduler.add_job(
                    func=self.check_model_job,
                    trigger="cron",
                    hour=4,
                    minute=0,
                    id="telemetry_check",
                    replace_existing=True,
                )
                logger.info("Telemetry Manager scheduled jobs (APScheduler)")
            except Exception as e:
                logger.error(f"Failed to schedule telemetry jobs: {e}")
        else:
            logger.warning(
                "No scheduler provided to Telemetry Manager. Automatic tasks disabled."
            )

    def stop(self):
        self.running = False

    def get_status(self):
        """Return current telemetry status."""
        telemetry_config = config.get("telemetry", {})
        return {
            "enabled": telemetry_config.get("enabled", True),
            "installation_id": config.get("installation_id"),
            "server_url": telemetry_config.get("server_url"),
            "last_submission": telemetry_config.get("last_submission"),
            "last_model_check": telemetry_config.get("last_model_check"),
            "manual_downloads_today": self.manual_downloads_today,
            "version": get_current_version(),
        }

    def submit_data_job(self):
        """Scheduled job to submit data."""
        if not config.get("telemetry.enabled", True):
            return

        try:
            logger.info("Starting daily telemetry submission...")
            self.submit_data(hours=24)
        except Exception as e:
            logger.error(f"Telemetry submission job failed: {e}")

    def check_model_job(self):
        """Scheduled job to check and update model."""
        if not config.get("telemetry.enabled", True):
            return

        try:
            logger.info("Starting daily model update check...")
            self.download_and_install_model(manual=False)
        except Exception as e:
            logger.error(f"Model check job failed: {e}")

    def submit_data(self, hours=24):
        """
        Query VictoriaMetrics for data and submit to server.
        """
        server_url = config.get("telemetry.server_url", "https://collector.xerolux.de")
        auth_token = config.get("telemetry.auth_token")

        if not auth_token:
            logger.warning("Telemetry: No auth token configured. Skipping submission.")
            return False

        # 1. Fetch data from VictoriaMetrics
        metrics_url = config.get("metrics.url", "http://victoriametrics:8428/write")
        base_url = metrics_url.replace("/write", "").replace("/api/v1/write", "")
        query_url = f"{base_url}/api/v1/export"

        # Time range
        end_ts = int(time.time())
        start_ts = end_ts - (hours * 3600)

        # Use export API to get raw data points for idm_heatpump metrics
        params = {
            "match[]": '{__name__=~"idm_heatpump_.*"}',
            "start": start_ts,
            "end": end_ts,
        }

        # Note: export API returns JSON stream (one object per line)
        try:
            logger.debug(f"Querying metrics from {query_url}")
            response = requests.get(query_url, params=params, stream=True, timeout=60)

            if response.status_code != 200:
                logger.error(f"Failed to query metrics: {response.status_code}")
                return False

            measurement_map = {}  # timestamp -> {metric: value}

            # Process stream
            count = 0
            for line in response.iter_lines():
                if not line:
                    continue
                try:
                    record = json.loads(line)
                    # format: {"metric":{"__name__":"...","tag":"..."},"values":[v1...],"timestamps":[t1...]}
                    # OR format: {"metric":..., "value":..., "timestamps":...} depending on version/flags?
                    # VM export API usually returns: {"metric":{"__name__":"name", ...}, "values":[...], "timestamps":[...]}

                    metric_name = (
                        record.get("metric", {})
                        .get("__name__", "")
                        .replace("idm_heatpump_", "")
                    )
                    values = record.get("values", [])
                    timestamps = record.get("timestamps", [])

                    if not metric_name:
                        continue

                    for t, v in zip(timestamps, values):
                        # t is usually ms in VM export? Check VM docs.
                        # VM export returns timestamps in milliseconds usually.
                        ts_sec = t / 1000.0

                        # Group by timestamp (bucket to nearest second to align)
                        ts_key = int(ts_sec)

                        if ts_key not in measurement_map:
                            measurement_map[ts_key] = {"timestamp": ts_sec}

                        measurement_map[ts_key][metric_name] = v
                        count += 1

                except Exception:
                    continue

            logger.info(
                f"Processed {count} data points into {len(measurement_map)} records."
            )

            if not measurement_map:
                logger.warning("No data found to submit.")
                return False

            # Convert map to list
            payload_data = list(measurement_map.values())

            # Batching (e.g. 5000 records per request)
            BATCH_SIZE = 5000
            total_batches = (len(payload_data) + BATCH_SIZE - 1) // BATCH_SIZE

            headers = {
                "Authorization": f"Bearer {auth_token}",
                "Content-Type": "application/json",
            }

            success_count = 0

            for i in range(0, len(payload_data), BATCH_SIZE):
                batch = payload_data[i : i + BATCH_SIZE]

                payload = {
                    "installation_id": config.get("installation_id"),
                    "heatpump_model": config.get("hp_model", "Unknown"),
                    "version": get_current_version(),
                    "data": batch,
                }

                try:
                    res = requests.post(
                        f"{server_url}/api/v1/submit",
                        json=payload,
                        headers=headers,
                        timeout=30,
                    )
                    if res.status_code in (200, 204):
                        success_count += 1
                    else:
                        logger.error(
                            f"Submit batch {i // BATCH_SIZE + 1} failed: {res.status_code} - {res.text}"
                        )
                except Exception as e:
                    logger.error(f"Submit batch {i // BATCH_SIZE + 1} error: {e}")

            if success_count == total_batches:
                config.set("telemetry.last_submission", int(time.time()))
                config.save()
                logger.info("Telemetry submission completed successfully.")
                return True
            else:
                logger.warning(
                    f"Telemetry submission partially failed ({success_count}/{total_batches} batches)."
                )
                return False

        except Exception as e:
            logger.error(f"Telemetry submission failed: {e}")
            return False

    def download_and_install_model(self, manual=False):
        """
        Check for model update, download if available, install to ML service.
        """
        # Rate limit check for manual
        if manual:
            if self.manual_downloads_today >= 3:
                logger.warning("Manual download limit reached.")
                raise Exception(
                    "Tägliches Limit für manuelle Downloads erreicht (3/Tag)."
                )

        server_url = config.get("telemetry.server_url", "https://collector.xerolux.de")
        installation_id = config.get("installation_id")
        hp_model = config.get("hp_model")

        # 1. Check eligibility
        try:
            check_url = f"{server_url}/api/v1/model/check"
            params = {"installation_id": installation_id, "model": hp_model}

            resp = requests.get(check_url, params=params, timeout=10)
            resp.raise_for_status()
            status = resp.json()

            config.set("telemetry.last_model_check", int(time.time()))
            config.save()

            if not status.get("eligible"):
                msg = status.get("reason_de", status.get("reason", "Nicht berechtigt"))
                logger.info(f"Model check: Not eligible - {msg}")
                if manual:
                    raise Exception(msg)
                return False

            if not status.get("model_available"):
                msg = status.get(
                    "reason_de", status.get("reason", "Kein Modell verfügbar")
                )
                logger.info(f"Model check: {msg}")
                if manual:
                    raise Exception(msg)
                return False

            if not status.get("update_available") and not manual:
                logger.info("Model check: No update needed.")
                return True

            # 2. Download Model
            logger.info("Downloading community model...")
            auth_token = config.get("telemetry.auth_token")
            headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}

            download_url = f"{server_url}/api/v1/model/download"
            resp = requests.get(
                download_url, params=params, headers=headers, timeout=60
            )
            resp.raise_for_status()

            # 3. Decrypt and Verify
            envelope = resp.json()

            # Verify signature
            key = DEFAULT_ENCRYPTION_KEY
            payload_b64 = envelope["payload"]
            metadata = envelope["metadata"]
            signature = envelope["signature"]

            # Reconstruct message to sign
            metadata_json = json.dumps(metadata, sort_keys=True)
            msg = f"{payload_b64}.{metadata_json}".encode("utf-8")

            expected_sig = hmac.new(key, msg, hashlib.sha256).hexdigest()

            if not hmac.compare_digest(expected_sig, signature):
                raise Exception("Ungültige Signatur des Modells! Download abgebrochen.")

            # Decrypt
            f = Fernet(key)
            encrypted_data = base64.b64decode(payload_b64)
            decrypted_data = f.decrypt(encrypted_data)

            # 4. Upload to ML Service
            logger.info("Uploading model to ML Service...")
            files = {"file": ("model_state.pkl", decrypted_data)}

            # Add internal secret header if configured
            ml_headers = {}
            internal_key = config.get("internal_api_key")
            if internal_key:
                ml_headers["X-Internal-Secret"] = internal_key

            upload_resp = requests.post(
                ML_SERVICE_UPLOAD_URL, files=files, headers=ml_headers, timeout=30
            )

            if upload_resp.status_code == 200:
                logger.info("Model installed successfully.")
                if manual:
                    self.manual_downloads_today += 1
                    self.last_manual_download = int(time.time())
                    self._save_state()
                return True
            else:
                raise Exception(f"ML Service Upload failed: {upload_resp.text}")

        except Exception as e:
            logger.error(f"Model update failed: {e}")
            if manual:
                raise e
            return False


telemetry_manager = TelemetryManager()
