
import sys
import os
import logging
from unittest.mock import MagicMock, patch

# Configure logging to show us what's happening
logging.basicConfig(level=logging.INFO)

# Add repo root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Mock dependencies
sys.modules['schedule'] = MagicMock()
sys.modules['flask'] = MagicMock()
sys.modules['requests'] = MagicMock()
# We need real river for the logic to actually calculate a score
# If river is not installed in this environment, we might need to mock it too,
# but the user asked if the *value* comes. Ideally we use real river.
# Let's try to see if river is importable. If not, we mock the model to return a fixed score.

try:
    import river
    print("River module found. Using real model logic.")
except ImportError:
    print("River module NOT found. Mocking model logic.")
    sys.modules['river'] = MagicMock()
    sys.modules['river.anomaly'] = MagicMock()
    sys.modules['river.preprocessing'] = MagicMock()
    sys.modules['river.compose'] = MagicMock()

# Patch env vars
with patch.dict(os.environ, {
    "METRICS_URL": "http://mock-vm:8428",
    "MIN_DATA_RATIO": "0.1", # The relaxed value
    "MODEL_PATH": "/tmp/test_model_verify.pkl"
}):
    from ml_service import main

# Mock the network calls
def mock_post(url, data=None, **kwargs):
    if "/write" in url:
        print("\n[SUCCESS] write_metrics called!")
        print(f"Target URL: {url}")
        print("Payload Data:")
        print("-" * 40)
        print(data)
        print("-" * 40)

        # Verify specific fields exist
        if "idm_anomaly_score" in data:
            print(">> CHECK PASS: 'idm_anomaly_score' is present.")
        else:
            print(">> CHECK FAIL: 'idm_anomaly_score' is MISSING.")

        return MagicMock(status_code=204)
    return MagicMock(status_code=200)

def mock_get(url, params=None, **kwargs):
    # Mock fetching data - return only ONE sensor to simulate "sparse" data
    # This would fail with the old code (needs ~0.4 * 5 = 2 sensors)
    # But should pass with the new code (needs 0.1 * 5 = 0.5 -> 1 sensor)
    if "query" in params:
        return MagicMock(status_code=200, json=lambda: {
            "status": "success",
            "data": {
                "result": [
                    {
                        "metric": {"__name__": "idm_heatpump_temp_flow"},
                        "value": [1234567890, "45.2"]
                    }
                ]
            }
        })
    return MagicMock(status_code=200)

# Apply mocks
main.requests.post = mock_post
main.requests.get = mock_get

# Force a known list of sensors so we know the ratio
main.SENSORS = ["temp_flow", "temp_return", "temp_outdoor", "power_in", "power_out"]

print(f"Test Configuration:")
print(f"- Total Sensors: {len(main.SENSORS)}")
print(f"- Min Data Ratio: {main.MIN_DATA_RATIO}")
print(f"- Mocking availability of ONLY 'temp_flow' (1 sensor)")
print("Running job()...\n")

# Run the job
try:
    # If river was mocked, we need to ensure model.score_one works
    if isinstance(main.model, MagicMock):
        main.model.score_one.return_value = 0.1234

    main.job()
except Exception as e:
    print(f"Job failed with exception: {e}")
