# Xerolux 2026
import unittest
from unittest.mock import MagicMock, patch
import json
import base64
import hmac
import hashlib
import os
import sys

# Add the project directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# -----------------------------------------------------------------------------
# Mock idm_logger.config to avoid side effects during import
# -----------------------------------------------------------------------------
mock_config_module = MagicMock()
sys.modules["idm_logger.config"] = mock_config_module

# Mock the 'config' instance that telemetry imports
mock_config_instance = MagicMock()
mock_config_module.config = mock_config_instance

# Mock Config class
mock_config_module.Config = MagicMock(return_value=mock_config_instance)

# Now we can safely import telemetry
from idm_logger.telemetry import TelemetryManager, DEFAULT_ENCRYPTION_KEY  # noqa: E402


class TestTelemetry(unittest.TestCase):
    def setUp(self):
        self.tm = TelemetryManager()
        # Reset rate limits
        self.tm.manual_downloads_today = 0
        self.tm.last_manual_download = 0

    @patch("idm_logger.telemetry.requests")
    # We don't need to patch 'idm_logger.telemetry.config' anymore because
    # we already mocked the module it imports from.
    # However, existing tests rely on 'mock_config' argument.
    # We can just use the globally mocked instance or patch it again for per-test isolation.
    def test_submit_data_success(self, mock_requests):
        # Configure the global mock config for this test
        mock_config_instance.get.side_effect = lambda k, d=None: {
            "telemetry.enabled": True,
            "telemetry.server_url": "http://test-server",
            "telemetry.auth_token": "token",
            "metrics.url": "http://vm:8428/write",
            "installation_id": "uuid",
            "hp_model": "TestModel",
        }.get(k, d)

        # Mock VM Export response
        mock_response_vm = MagicMock()
        mock_response_vm.status_code = 200
        mock_response_vm.iter_lines.return_value = [
            json.dumps(
                {
                    "metric": {"__name__": "idm_heatpump_temp"},
                    "values": [20.5],
                    "timestamps": [1000],
                }
            ).encode(),
        ]

        # Mock Server Submit response
        mock_response_server = MagicMock()
        mock_response_server.status_code = 200

        mock_requests.get.return_value = mock_response_vm
        mock_requests.post.return_value = mock_response_server

        # Run
        success = self.tm.submit_data()

        self.assertTrue(success)
        mock_requests.get.assert_called()
        mock_requests.post.assert_called()

        args, kwargs = mock_requests.post.call_args
        self.assertEqual(args[0], "http://test-server/api/v1/submit")

    @patch("idm_logger.telemetry.requests")
    def test_submit_data_batching(self, mock_requests):
        mock_config_instance.get.side_effect = lambda k, d=None: {
            "telemetry.enabled": True,
            "telemetry.server_url": "http://test-server",
            "telemetry.auth_token": "token",
            "metrics.url": "http://vm:8428/write",
            "installation_id": "uuid",
            "hp_model": "TestModel",
        }.get(k, d)

        # 250 records
        records = []
        for i in range(250):
            records.append(
                json.dumps(
                    {
                        "metric": {"__name__": "idm_heatpump_temp"},
                        "values": [i],
                        "timestamps": [i * 1000],
                    }
                ).encode()
            )

        mock_response_vm = MagicMock()
        mock_response_vm.status_code = 200
        mock_response_vm.iter_lines.return_value = records
        mock_requests.get.return_value = mock_response_vm
        mock_requests.post.return_value = MagicMock(status_code=200)

        # Run
        success = self.tm.submit_data()

        self.assertTrue(success)
        self.assertEqual(mock_requests.post.call_count, 2)

    @patch("idm_logger.telemetry.requests")
    def test_download_model_success(self, mock_requests):
        mock_config_instance.get.side_effect = lambda k, d=None: {
            "installation_id": "uuid",
            "hp_model": "TestModel",
            "telemetry.server_url": "http://test-server",
            "internal_api_key": "secret",
        }.get(k, d)

        # Responses
        mock_resp_check = MagicMock()
        mock_resp_check.status_code = 200
        mock_resp_check.json.return_value = {
            "eligible": True,
            "model_available": True,
            "update_available": True,
        }

        # Encrypted Model
        try:
            # We need cryptography here since we imported it (or rely on it being installed)
            from cryptography.fernet import Fernet
            key = DEFAULT_ENCRYPTION_KEY
            f = Fernet(key)
            original_data = b"serialized_model_data"
            encrypted_data = f.encrypt(original_data)
            payload_b64 = base64.b64encode(encrypted_data).decode("utf-8")
        except ImportError:
            # Fallback if cryptography not installed (though we installed it)
            self.skipTest("cryptography module missing")

        metadata = {"filename": "model.pkl"}
        metadata_json = json.dumps(metadata, sort_keys=True)
        msg = f"{payload_b64}.{metadata_json}".encode("utf-8")
        signature = hmac.new(key, msg, hashlib.sha256).hexdigest()

        envelope = {
            "payload": payload_b64,
            "metadata": metadata,
            "signature": signature,
        }

        mock_resp_download = MagicMock()
        mock_resp_download.status_code = 200
        mock_resp_download.json.return_value = envelope

        mock_resp_upload = MagicMock()
        mock_resp_upload.status_code = 200

        mock_requests.get.side_effect = [mock_resp_check, mock_resp_download]
        mock_requests.post.return_value = mock_resp_upload

        # Run
        success = self.tm.download_and_install_model(manual=True)

        self.assertTrue(success)

    def test_rate_limit(self):
        self.tm.manual_downloads_today = 3
        with self.assertRaises(Exception) as cm:
            self.tm.download_and_install_model(manual=True)
        self.assertIn("Limit", str(cm.exception))

    @patch("idm_logger.telemetry.requests")
    def test_admin_status_update(self, mock_requests):
        """Test that is_admin status is correctly updated from server response."""
        mock_config_instance.get.side_effect = lambda k, d=None: {
            "installation_id": "uuid",
            "hp_model": "TestModel",
            "telemetry.server_url": "http://test-server",
        }.get(k, d)

        # Case 1: Server says is_admin = True
        mock_resp_check_true = MagicMock()
        mock_resp_check_true.status_code = 200
        mock_resp_check_true.json.return_value = {
            "eligible": True,
            "model_available": False,
            "update_available": False,
            "is_admin": True,
            "server_stats": {"active_installations": 10},
        }

        mock_requests.get.return_value = mock_resp_check_true

        # Run
        try:
            self.tm.download_and_install_model(manual=True)
        except Exception:
            pass  # Expected because model_available=False

        # Verify
        self.assertTrue(self.tm.is_admin)
        self.assertEqual(self.tm.server_stats["active_installations"], 10)

        # Case 2: Server says is_admin = False
        mock_resp_check_false = MagicMock()
        mock_resp_check_false.status_code = 200
        mock_resp_check_false.json.return_value = {
            "eligible": True,
            "model_available": False,
            "update_available": False,
            "is_admin": False,
        }

        mock_requests.get.return_value = mock_resp_check_false

        # Run again
        try:
            self.tm.download_and_install_model(manual=True)
        except Exception:
            pass

        # Verify
        self.assertFalse(self.tm.is_admin)
        self.assertIsNone(self.tm.server_stats)


if __name__ == "__main__":
    unittest.main()
