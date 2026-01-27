import os
from unittest.mock import patch, MagicMock
import sys

# Mock idm_logger.db before importing config
mock_db_module = MagicMock()
mock_db_instance = MagicMock()
# Configure get_setting to return None by default so _load_data returns defaults
mock_db_instance.get_setting.return_value = None
mock_db_module.db = mock_db_instance
sys.modules["idm_logger.db"] = mock_db_module

# Now we can safely import Config
from idm_logger.config import Config  # noqa: E402


class TestSentinelAdminAuth:
    def setup_method(self):
        # Reset environment variables before each test
        self._env_patch = patch.dict(os.environ, clear=True)
        self._env_patch.start()

    def teardown_method(self):
        self._env_patch.stop()

    def test_fail_closed_no_hash(self):
        """Verify that with no hash set, checking any password (including 'admin') returns False."""
        # Instantiate Config
        config = Config()

        # Ensure no hash is present (in case defaults change)
        if "admin_password_hash" in config.data["web"]:
            del config.data["web"]["admin_password_hash"]

        assert config.check_admin_password("admin") is False
        assert config.check_admin_password("secret") is False
        assert config.check_admin_password("") is False

    def test_admin_password_env_var(self):
        """Verify that ADMIN_PASSWORD environment variable sets the hash correctly."""
        test_password = "secure_password_123"
        with patch.dict(os.environ, {"ADMIN_PASSWORD": test_password}):
            config = Config()

            # Check if hash was generated
            assert "admin_password_hash" in config.data["web"]

            # Check if password works
            assert config.check_admin_password(test_password) is True
            assert config.check_admin_password("wrong_password") is False
            assert config.check_admin_password("admin") is False

    def test_existing_hash_respected(self):
        """Verify that an existing hash is respected."""
        from werkzeug.security import generate_password_hash

        existing_pass = "existing_secret"
        hashed = generate_password_hash(existing_pass)

        # We patch _load_data to simulate reading from DB/file
        with patch.object(Config, "_load_data") as mock_load:
            # Create a mock data structure mimicking what _load_data returns
            # We must provide all keys that __init__ might access or merge
            mock_data = {
                "web": {
                    "admin_password_hash": hashed,
                    "enabled": True,
                    "host": "0.0.0.0",
                    "port": 5000,
                    "write_enabled": False,
                },
                "idm": {},
                "metrics": {},
                "network_security": {},
                "logging": {},
                "mqtt": {},
                "signal": {},
                "telegram": {},
                "discord": {},
                "email": {},
                "webdav": {},
                "ai": {},
                "updates": {},
                "backup": {},
                "internal_api_key": None,
                "setup_completed": True,
            }
            mock_load.return_value = mock_data

            config = Config()

            assert config.check_admin_password(existing_pass) is True
            assert config.check_admin_password("admin") is False

    def test_partial_setup_metrics_only(self):
        """Verify that METRICS_URL alone does NOT complete setup if password is missing."""
        # Mock only METRICS_URL
        with patch.dict(os.environ, {"METRICS_URL": "http://influx:8086"}):
            config = Config()
            # Should be False because no password was provided
            assert config.is_setup() is False
            # Check password check fails (fail closed)
            assert config.check_admin_password("admin") is False

    def test_full_setup_via_env(self):
        """Verify that METRICS_URL + ADMIN_PASSWORD completes setup."""
        with patch.dict(os.environ, {
            "METRICS_URL": "http://influx:8086",
            "ADMIN_PASSWORD": "mysecretpassword"
        }):
            config = Config()
            assert config.is_setup() is True
            assert config.check_admin_password("mysecretpassword") is True
