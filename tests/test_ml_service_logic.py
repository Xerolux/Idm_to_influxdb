import unittest
from unittest.mock import MagicMock, patch, mock_open
import sys
import os
import importlib
import pickle

# Add repo root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class TestMLServiceLogic(unittest.TestCase):
    def setUp(self):
        # We need to ensure we can import ml_service.main
        self.env_patcher = patch.dict(
            os.environ,
            {
                "METRICS_URL": "http://test-vm",
                "MIN_DATA_RATIO": "0.4",
                "MODEL_PATH": "/tmp/test_model.pkl",
            },
        )
        self.env_patcher.start()

        # Import or reload main to pick up env vars and reset state
        import ml_service.main as main

        importlib.reload(main)
        self.main = main

        # Reset globals
        self.main.SENSORS = ["sensor1", "sensor2", "sensor3", "sensor4", "sensor5"]

        # Mock the model
        self.main.model = MagicMock()
        self.main.logger = MagicMock()

    def tearDown(self):
        self.env_patcher.stop()

    def test_job_proceeds_with_partial_data(self):
        """Test that job() proceeds even if data count < min_features."""
        with (
            patch.object(self.main, "fetch_latest_data") as mock_fetch,
            patch.object(self.main, "write_metrics") as mock_write,
            patch.object(self.main, "enrich_features") as mock_enrich,
        ):
            mock_fetch.return_value = {"sensor1": 10.0}  # Only 1 sensor
            mock_enrich.return_value = {"sensor1": 10.0, "extra": 1}  # Enriched

            self.main.model.score_one.return_value = 0.5

            # Run job
            self.main.job()

            # Verify warnings were logged
            self.main.logger.warning.assert_called()
            args, _ = self.main.logger.warning.call_args
            self.assertIn("Low data availability", args[0])

            # Verify metrics WERE written
            mock_write.assert_called_once()

            # Verify model was updated
            self.main.model.learn_one.assert_called_once()

    def test_job_aborts_on_no_data(self):
        """Test that job() aborts if NO data is fetched (empty dict or None)."""
        with (
            patch.object(self.main, "fetch_latest_data") as mock_fetch,
            patch.object(self.main, "write_metrics") as mock_write,
        ):
            mock_fetch.return_value = {}  # Empty dict

            self.main.job()

            # Should not write metrics
            mock_write.assert_not_called()
            self.main.model.learn_one.assert_not_called()

    def test_persistence_pickle(self):
        """Test save and load model state using pickle (mocked)."""
        # Force USE_JOBLIB to False for this test
        self.main.USE_JOBLIB = False
        self.main.model = "test_model_obj"

        # Inject pickle module if not present (because joblib might have been preferred)
        if not hasattr(self.main, "pickle"):
            self.main.pickle = pickle

        # Test Save
        with (
            patch("builtins.open", mock_open()) as m,
            patch("pickle.dump") as mock_dump,
        ):
            self.main.save_model_state()
            m.assert_called_with(self.main.MODEL_PATH, "wb")
            # Check if pickle.dump was called with the model object
            mock_dump.assert_called()
            args, _ = mock_dump.call_args
            self.assertEqual(args[0], "test_model_obj")

        # Test Load
        with (
            patch("os.path.exists", return_value=True),
            patch("builtins.open", mock_open(read_data=b"data")),
            patch("pickle.load", return_value="loaded_model"),
        ):
            res = self.main.load_model_state()
            self.assertTrue(res)
            self.assertEqual(self.main.model, "loaded_model")


if __name__ == "__main__":
    unittest.main()
