import logging
import datetime
import time
import requests
from .config import config

# Import at top level as it is a core dependency now
try:
    from influxdb_client_3 import InfluxDBClient3, Point, WriteOptions
except ImportError:
    # Fallback/logging if not installed, though it should be
    InfluxDBClient3 = None
    Point = None
    WriteOptions = None

logger = logging.getLogger(__name__)

# Retry configuration
MAX_RETRIES = 3
RETRY_DELAY_BASE = 2  # seconds, exponential backoff


class InfluxWriter:
    def __init__(self):
        self.conf = config.get("influx")
        self.client = None
        self.bucket = None
        self.url = None
        self.token = None
        self._connected = False
        self._last_error = None
        self._use_v3_api = True  # Use native v3 API by default
        self._setup_with_retry()

    def _setup_with_retry(self):
        """Setup InfluxDB connection with retry logic."""
        for attempt in range(MAX_RETRIES):
            try:
                self._setup()
                # InfluxDB 3 client doesn't explicitly connect until first request,
                # but we assume success if no exception during init.
                # We can try a dummy query or health check if API allows.
                self._connected = True
                logger.info(f"InfluxDB 3 client initialized")
                return
            except Exception as e:
                self._last_error = str(e)
                delay = RETRY_DELAY_BASE ** (attempt + 1)
                logger.warning(
                    f"InfluxDB connection attempt {attempt + 1}/{MAX_RETRIES} failed: {e}. "
                    f"Retrying in {delay}s..."
                )
                if attempt < MAX_RETRIES - 1:
                    time.sleep(delay)

        logger.error(f"Failed to connect to InfluxDB after {MAX_RETRIES} attempts")

    def _setup(self):
        """Initialize InfluxDB 3 client."""
        self._connected = False

        # User's v3 Core configuration uses port 8181
        self.url = self.conf.get("url", "http://localhost:8181")
        self.token = self.conf.get("token", "")
        org = self.conf.get("org", "")
        self.bucket = self.conf.get("bucket", "idm")

        if not self.token or not self.url:
            logger.warning("InfluxDB URL or token not configured")
            return

        if self._use_v3_api:
            # For v3 API, we don't need the influxdb3-python client for writes
            # We'll use direct HTTP requests to /api/v3/write_lp
            logger.info("Using native InfluxDB v3 API (/api/v3/write_lp)")

            # Still initialize client for queries (uses Flight SQL)
            if InfluxDBClient3 is not None:
                self.client = InfluxDBClient3(
                    host=self.url,
                    token=self.token,
                    org=org,
                    database=self.bucket
                )
        else:
            # Use influxdb3-python library (v2 compatibility mode)
            if InfluxDBClient3 is None:
                raise ImportError("influxdb3-python not installed")

            self.client = InfluxDBClient3(
                host=self.url,
                token=self.token,
                org=org,
                database=self.bucket
            )

        # Ensure database exists in InfluxDB v3
        self._ensure_database_exists()

    def _ensure_database_exists(self):
        """Ensure the database (bucket) exists in InfluxDB v3."""
        try:
            # In InfluxDB 3 Core, databases are created automatically on first write
            # We don't need to explicitly create them, which avoids auth issues during setup
            logger.info(f"Database '{self.bucket}' will be auto-created on first write")
        except Exception as e:
            logger.debug(f"Database setup note: {e}")

    def is_connected(self) -> bool:
        """Return current connection status."""
        return self._connected

    def get_status(self) -> dict:
        """Get detailed status information."""
        return {
            "connected": self._connected,
            "version": 3,
            "url": self.conf.get("url", ""),
            "bucket": self.conf.get("bucket", ""),
            "last_error": self._last_error
        }

    def reconnect(self):
        """Attempt to reconnect to InfluxDB."""
        logger.info("Attempting to reconnect to InfluxDB...")
        self._close()
        self._setup_with_retry()

    def _close(self):
        """Close existing connection."""
        if self.client:
            try:
                self.client.close()
            except Exception:
                pass
        self.client = None
        self._connected = False

    def write(self, measurements: dict) -> bool:
        """Write measurements to InfluxDB with error handling and retry."""
        if not measurements:
            return True

        if not self.client:
            if not self._connected:
                self.reconnect()
            if not self.client:
                return False

        for attempt in range(MAX_RETRIES):
            try:
                success = self._write_internal(measurements)
                if success:
                    return True
            except Exception as e:
                self._last_error = str(e)
                delay = RETRY_DELAY_BASE ** attempt
                logger.warning(
                    f"InfluxDB write attempt {attempt + 1}/{MAX_RETRIES} failed: {e}"
                )
                if attempt < MAX_RETRIES - 1:
                    time.sleep(delay)
                else:
                    logger.error(f"InfluxDB write failed after {MAX_RETRIES} attempts")
                    # Don't mark disconnected immediately on write failure for v3 as it might be transient
                    # But if persistent, maybe?
                    # For now, keep connected state unless re-init needed.

        return False

    def _write_internal(self, measurements: dict) -> bool:
        """Internal write method using InfluxDB 3 API."""
        if self._use_v3_api:
            # Use native v3 API with direct HTTP request
            return self._write_v3_api(measurements)
        else:
            # Use influxdb3-python library (v2 compatibility)
            return self._write_v2_compat(measurements)

    def _write_v3_api(self, measurements: dict) -> bool:
        """Write using native InfluxDB v3 API endpoint /api/v3/write_lp."""
        import time as time_module

        # Build line protocol string manually
        # Format: measurement[,tag=value] field=value[,field2=value2] [timestamp]
        measurement_name = "idm_heatpump"

        # Collect fields and build line protocol
        fields = []
        for key, value in measurements.items():
            # Skip string representation fields
            if key.endswith("_str"):
                continue
            # Convert booleans to int
            if isinstance(value, bool):
                value = int(value)
            # Only write numeric values as fields
            if isinstance(value, (int, float)):
                # Properly format field values for line protocol
                # Integers need 'i' suffix, floats don't
                if isinstance(value, int) and not isinstance(value, bool):
                    fields.append(f"{key}={value}i")
                else:
                    fields.append(f"{key}={value}")

        if not fields:
            return False

        # Build line protocol string with proper spacing
        timestamp = int(time_module.time() * 1e9)
        line_protocol = f"{measurement_name} {','.join(fields)} {timestamp}"

        # Make HTTP POST request to v3 write endpoint
        try:
            write_url = f"{self.url}/api/v3/write_lp"
            params = {"db": self.bucket}
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "text/plain; charset=utf-8"
            }

            response = requests.post(
                write_url,
                params=params,
                headers=headers,
                data=line_protocol,
                timeout=10
            )

            if response.status_code in (204, 200):
                return True
            else:
                logger.warning(
                    f"Write failed with status {response.status_code}: {response.text}"
                )
                return False

        except Exception as e:
            raise Exception(f"({getattr(e, 'response', type(e).__name__)})\n"
                          f"Reason: {str(e)}")

    def _write_v2_compat(self, measurements: dict) -> bool:
        """Write using influxdb3-python library (v2 compatibility mode)."""
        if Point is None:
            return False

        # Create a point
        p = Point("idm_heatpump")

        # Add fields - let the library handle timestamp automatically
        has_fields = False
        for key, value in measurements.items():
            # Skip string representation fields
            if key.endswith("_str"):
                continue
            # Convert booleans to int
            if isinstance(value, bool):
                value = int(value)
            # Only write numeric values as fields
            if isinstance(value, (int, float)):
                p = p.field(key, value)
                has_fields = True

        if has_fields:
            self.client.write(p)
            return True

        return False

    def query(self, query: str, language: str = "sql") -> list:
        """Execute a query (default SQL). Returns list of dicts or values."""
        if not self.client:
            return []

        try:
            # query() returns a PyArrow Table (default) or Pandas DataFrame
            # We want simple list of dicts for compatibility with app usage if any.
            # But wait, app doesn't use query() results except maybe for debugging?
            # Actually, nothing uses query() return value in the python code we grepped.
            # But let's implement it to return list of rows (dicts) just in case.

            table = self.client.query(query=query, language=language)
            # Convert PyArrow table to list of dicts
            return table.to_pylist()
        except Exception as e:
            logger.error(f"InfluxDB query failed: {e}")
            return []

    def delete_all_data(self) -> bool:
        """Delete all data from the database (bucket)."""
        if not self.client:
            return False

        try:
            # InfluxDB 3 (IOx) supports standard SQL.
            # "DROP TABLE idm_heatpump" is the standard way to clear a measurement.
            self.client.query(query="DROP TABLE idm_heatpump", language="sql")
            logger.info("Deleted all data (DROP TABLE idm_heatpump)")
            return True
        except Exception as e:
            logger.error(f"Failed to delete data: {e}")
            return False

    def __del__(self):
        """Cleanup on destruction."""
        self._close()
