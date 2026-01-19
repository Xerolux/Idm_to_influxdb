# SPDX-License-Identifier: MIT
import logging
import requests
import os
import queue
import threading
import time
from .config import config

logger = logging.getLogger(__name__)


class MetricsWriter:
    def __init__(self):
        self.url = os.environ.get(
            "METRICS_URL",
            config.get("metrics.url", "http://victoriametrics:8428/write"),
        )
        self._connected = True  # HTTP is stateless
        self.session = requests.Session()

        # Async queue for metrics to avoid blocking main loop
        self.queue = queue.Queue(maxsize=1000)
        self.stop_event = threading.Event()
        self.worker_thread = threading.Thread(target=self._worker, daemon=True)
        self.worker_thread.start()

        logger.info(f"MetricsWriter initialized with URL: {self.url} (Async)")

    def is_connected(self) -> bool:
        return self._connected

    def write(self, measurements: dict) -> bool:
        if not measurements:
            return True

        try:
            self.queue.put_nowait(measurements)
            return True
        except queue.Full:
            logger.warning("Metrics queue full, dropping data")
            return False

    def _worker(self):
        """Worker thread to process metrics queue."""
        batch = []
        last_flush_time = time.time()
        BATCH_SIZE = 50
        BATCH_TIMEOUT = 1.0

        while not self.stop_event.is_set():
            try:
                # Calculate how long to wait for the next item
                time_since_last_flush = time.time() - last_flush_time
                if batch:
                    # If we have items, wait only until the timeout expires
                    wait_time = max(0.1, BATCH_TIMEOUT - time_since_last_flush)
                else:
                    # If empty, wait up to 1s (to check stop_event periodically)
                    wait_time = 1.0

                measurements = self.queue.get(timeout=wait_time)
                batch.append(measurements)
                self.queue.task_done()
            except queue.Empty:
                pass

            # Check flush conditions
            current_time = time.time()
            if batch and (
                len(batch) >= BATCH_SIZE
                or (current_time - last_flush_time) >= BATCH_TIMEOUT
            ):
                try:
                    self._send_batch(batch)
                except Exception as e:
                    logger.error(f"Error in metrics worker: {e}")
                finally:
                    batch = []
                    last_flush_time = current_time

        # Flush remaining items on stop
        if batch:
            try:
                self._send_batch(batch)
            except Exception as e:
                logger.error(f"Error in metrics worker flushing on stop: {e}")

    def _send_batch(self, batch: list) -> bool:
        """Internal method to send data to VictoriaMetrics (executed in worker thread)."""
        lines = []
        for measurements in batch:
            measurement = "idm_heatpump"
            fields = []

            for key, value in measurements.items():
                # Skip string representation fields
                if key.endswith("_str"):
                    continue
                # Convert booleans to int
                if isinstance(value, bool):
                    value = int(value)
                # Only write numeric values
                if isinstance(value, (int, float)):
                    fields.append(f"{key}={value}")

            if fields:
                field_str = ",".join(fields)
                lines.append(f"{measurement} {field_str}")

        if not lines:
            return False

        payload = "\n".join(lines)

        try:
            # VictoriaMetrics /write endpoint
            # Use session for connection pooling
            response = self.session.post(self.url, data=payload, timeout=5)
            if response.status_code in (200, 204):
                return True
            else:
                logger.error(
                    f"Failed to write metrics: {response.status_code} {response.text}"
                )
                return False
        except Exception as e:
            logger.error(f"Exception writing metrics: {e}")
            return False

    def get_status(self) -> dict:
        return {
            "connected": self._connected,
            "type": "VictoriaMetrics",
            "url": self.url,
            "queue_size": self.queue.qsize()
        }

    def stop(self):
        """Stop the worker thread."""
        self.stop_event.set()
        self.worker_thread.join(timeout=2.0)
