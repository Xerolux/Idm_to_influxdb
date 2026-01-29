# Xerolux 2026
import unittest
from unittest.mock import MagicMock, patch
import json
import base64
import hmac
import hashlib
from cryptography.fernet import Fernet

# Mock config before importing telemetry
with patch("idm_logger.telemetry.config") as mock_config:
    mock_config.get.return_value = "mock_value"
    from idm_logger.telemetry import TelemetryManager, DEFAULT_ENCRYPTION_KEY

class TestTelemetry(unittest.TestCase):
    def setUp(self):
        self.tm = TelemetryManager()
        # Reset rate limits
        self.tm.manual_downloads_today = 0
        self.tm.last_manual_download = 0

    @patch("idm_logger.telemetry.requests")
    @patch("idm_logger.telemetry.config")
    def test_submit_data_success(self, mock_config, mock_requests):
        # Setup Config
        mock_config.get.side_effect = lambda k, d=None: {
            "telemetry.enabled": True,
            "telemetry.server_url": "http://test-server",
            "telemetry.auth_token": "token",
            "metrics.url": "http://vm:8428/write",
            "installation_id": "uuid",
            "hp_model": "TestModel"
        }.get(k, d)

        # Mock VM Export response (stream of JSON lines)
        mock_response_vm = MagicMock()
        mock_response_vm.status_code = 200
        mock_response_vm.iter_lines.return_value = [
            json.dumps({"metric": {"__name__": "idm_heatpump_temp"}, "values": [20.5], "timestamps": [1000]}).encode(),
            json.dumps({"metric": {"__name__": "idm_heatpump_power"}, "values": [1000], "timestamps": [1000]}).encode()
        ]

        # Mock Server Submit response
        mock_response_server = MagicMock()
        mock_response_server.status_code = 200

        mock_requests.get.return_value = mock_response_vm
        mock_requests.post.return_value = mock_response_server

        # Run
        success = self.tm.submit_data()

        self.assertTrue(success)
        mock_requests.get.assert_called() # VM Query
        mock_requests.post.assert_called() # Server Submit

        # Check payload
        args, kwargs = mock_requests.post.call_args
        self.assertEqual(args[0], "http://test-server/api/v1/submit")
        payload = kwargs['json']
        self.assertEqual(payload['installation_id'], "uuid")
        self.assertEqual(len(payload['data']), 1) # 1 timestamp bucket
        self.assertEqual(payload['data'][0]['temp'], 20.5)

    @patch("idm_logger.telemetry.requests")
    @patch("idm_logger.telemetry.config")
    def test_download_model_success(self, mock_config, mock_requests):
        mock_config.get.side_effect = lambda k, d=None: {
            "installation_id": "uuid",
            "hp_model": "TestModel",
            "telemetry.server_url": "http://test-server",
            "internal_api_key": "secret"
        }.get(k, d)

        # 1. Check Eligibility Response
        mock_resp_check = MagicMock()
        mock_resp_check.status_code = 200
        mock_resp_check.json.return_value = {
            "eligible": True,
            "model_available": True,
            "update_available": True
        }

        # 2. Prepare Encrypted Model
        key = DEFAULT_ENCRYPTION_KEY
        f = Fernet(key)
        original_data = b"serialized_model_data"
        encrypted_data = f.encrypt(original_data)
        payload_b64 = base64.b64encode(encrypted_data).decode("utf-8")

        metadata = {"filename": "model.pkl"}
        metadata_json = json.dumps(metadata, sort_keys=True)
        msg = f"{payload_b64}.{metadata_json}".encode("utf-8")
        signature = hmac.new(key, msg, hashlib.sha256).hexdigest()

        envelope = {
            "payload": payload_b64,
            "metadata": metadata,
            "signature": signature
        }

        mock_resp_download = MagicMock()
        mock_resp_download.status_code = 200
        mock_resp_download.json.return_value = envelope

        # 3. Upload Response
        mock_resp_upload = MagicMock()
        mock_resp_upload.status_code = 200

        # Mocking requests
        mock_requests.get.side_effect = [mock_resp_check, mock_resp_download]
        mock_requests.post.return_value = mock_resp_upload

        # Run
        success = self.tm.download_and_install_model(manual=True)

        self.assertTrue(success)

        # Verify Upload
        args, kwargs = mock_requests.post.call_args
        self.assertIn("file", kwargs['files'])
        uploaded_filename, uploaded_data = kwargs['files']['file']
        self.assertEqual(uploaded_filename, "model_state.pkl")
        self.assertEqual(uploaded_data, original_data)

    def test_rate_limit(self):
        self.tm.manual_downloads_today = 3
        with self.assertRaises(Exception) as cm:
            self.tm.download_and_install_model(manual=True)
        self.assertIn("Limit", str(cm.exception))

if __name__ == '__main__':
    unittest.main()
