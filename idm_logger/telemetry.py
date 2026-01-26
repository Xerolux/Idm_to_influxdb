# SPDX-License-Identifier: MIT
import logging
import requests
import threading
import time
import os
import random
from .config import config
from .update_manager import get_current_version
from .heatpump_manager import heatpump_manager

logger = logging.getLogger(__name__)

# Default telemetry endpoint
DEFAULT_ENDPOINT = "https://collector.xerolux.de/api/v1/submit"


class TelemetryManager:
    def __init__(self, config_instance):
        self.config = config_instance
        # Always prefer Environment Variable, but allow user to use default if not set
        # The user SHOULD set TELEMETRY_ENDPOINT in docker-compose
        self.endpoint = os.environ.get("TELEMETRY_ENDPOINT", DEFAULT_ENDPOINT)
        self._buffer = []
        self._lock = threading.Lock()
        self._send_interval = 86400  # Send every 24 hours (daily)
        # Initialize last_send with random offset to distribute load (avoid Thundering Herd)
        # This effectively picks a random time of day for the daily upload
        self._last_send = time.time() - random.randint(0, self._send_interval)
        self._max_buffer_size = 2000  # Force send if buffer gets too big
        self._worker_thread = None
        self._running = False

    def start(self):
        """Start the background worker."""
        if self._running:
            return
        self._running = True
        self._worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self._worker_thread.start()
        logger.info("Telemetry manager started")

    def stop(self):
        """Stop the background worker."""
        self._running = False
        if self._worker_thread:
            self._worker_thread.join(timeout=2)

    def submit_data(self, sensor_data):
        """Submit sensor data to be sent."""
        if not self.config.get("share_data", True):
            return

        # We allow sending if at least one heatpump is configured
        if not heatpump_manager.connection_count and not self.config.get(
            "heatpump_model"
        ):
            return

        with self._lock:
            # Add timestamp if not present
            if "timestamp" not in sensor_data:
                sensor_data["timestamp"] = time.time()
            self._buffer.append(sensor_data)

    def _worker_loop(self):
        while self._running:
            time.sleep(10)  # Check every 10 seconds

            if not self.config.get("share_data", True):
                with self._lock:
                    self._buffer.clear()  # Clear buffer if sharing is disabled
                continue

            now = time.time()
            should_send = False

            with self._lock:
                buffer_size = len(self._buffer)

            if now - self._last_send >= self._send_interval:
                should_send = True
            elif buffer_size >= self._max_buffer_size:
                logger.info(
                    f"Telemetry buffer full ({buffer_size} items), forcing flush"
                )
                should_send = True

            if should_send:
                self._flush_buffer()

    def _flush_buffer(self):
        with self._lock:
            if not self._buffer:
                return
            # Take copy of buffer
            raw_buffer = list(self._buffer)
            self._buffer.clear()

        try:
            configs = heatpump_manager.get_all_configs()

            # Process all data first
            processed_data = []
            for snapshot in raw_buffer:
                timestamp = snapshot.get("timestamp", time.time())

                is_nested = any(
                    isinstance(v, dict) for k, v in snapshot.items() if k != "timestamp"
                )

                if is_nested:
                    heatpumps_data = []
                    for hp_id, values in snapshot.items():
                        if hp_id == "timestamp":
                            continue
                        if not isinstance(values, dict):
                            continue

                        hp_config = configs.get(hp_id, {})
                        heatpumps_data.append(
                            {
                                "id": hp_id,
                                "manufacturer": hp_config.get(
                                    "manufacturer", "unknown"
                                ),
                                "model": hp_config.get("model", "unknown"),
                                "values": values,
                            }
                        )

                    processed_data.append(
                        {"timestamp": timestamp, "heatpumps": heatpumps_data}
                    )
                else:
                    processed_data.append(snapshot)

            # Send in chunks to avoid huge payloads
            BATCH_SIZE = 500
            total_records = len(processed_data)

            if total_records == 0:
                return

            for i in range(0, total_records, BATCH_SIZE):
                chunk = processed_data[i : i + BATCH_SIZE]
                self._send_batch(chunk, i + 1, total_records)

            self._last_send = time.time()

        except Exception as e:
            logger.error(f"Error preparing telemetry: {e}")
            # Note: Data is lost if processing fails, which is acceptable for telemetry
            # to avoid blocking/memory leaks loop.

    def _send_batch(self, data_chunk, start_idx, total):
        """Send a single batch of data."""
        payload = {
            "installation_id": self.config.get("installation_id"),
            "heatpump_model": self.config.get("heatpump_model"),
            "version": get_current_version(),
            "data_version": "2.0",
            "data": data_chunk,
            "batch_index": start_idx,
            "total_records": total,
        }

        try:
            if "example.com" in self.endpoint:
                logger.debug(
                    f"Telemetry (Simulation): Would send batch {len(data_chunk)} records to {self.endpoint}"
                )
                return

            headers = {}
            token = self.config.get("telemetry_auth_token")
            if token:
                headers["Authorization"] = f"Bearer {token}"

            response = requests.post(
                self.endpoint, json=payload, headers=headers, timeout=30
            )

            if response.status_code == 200:
                logger.debug(
                    f"Telemetry batch sent ({len(data_chunk)} records, {start_idx}-{start_idx + len(data_chunk) - 1}/{total})"
                )
            else:
                logger.warning(f"Telemetry batch send failed: {response.status_code}")

        except Exception as e:
            logger.error(f"Error sending telemetry batch: {e}")


# Global instance
telemetry_manager = TelemetryManager(config)
