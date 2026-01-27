import pytest
from unittest.mock import patch, MagicMock

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@patch("requests.post")
def test_submit_telemetry(mock_post, client):
    mock_post.return_value.status_code = 204

    payload = {
        "installation_id": "test-id",
        "heatpump_model": "test-model",
        "version": "1.0",
        "data": [
            {"timestamp": 1234567890, "temp": 20.5}
        ]
    }

    # Needs auth
    headers = {"Authorization": "Bearer test-token"}
    response = client.post("/api/v1/submit", json=payload, headers=headers)

    assert response.status_code == 200
    assert mock_post.called
    # Check Influx line protocol format
    args, kwargs = mock_post.call_args
    assert "heatpump_metrics" in kwargs["data"]
    assert "temp=20.5" in kwargs["data"]

def test_submit_telemetry_unauthorized(client):
    response = client.post("/api/v1/submit", json={})
    assert response.status_code == 401

@patch("requests.get")
def test_pool_status(mock_get, client):
    # Mock VM query responses
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "success",
        "data": {"result": [{"value": [123456, "10"]}]}
    }
    mock_get.return_value = mock_response

    response = client.get("/api/v1/pool/status")
    assert response.status_code == 200
    data = response.json()
    assert "total_installations" in data
    assert "total_data_points" in data
