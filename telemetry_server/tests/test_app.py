# Xerolux 2026
from unittest.mock import patch, MagicMock, AsyncMock
import pytest

# ... existing tests ...


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@patch("app.httpx.AsyncClient")
def test_submit_telemetry(mock_client_cls, client):
    # Mock AsyncClient context manager
    mock_instance = AsyncMock()
    mock_client_cls.return_value.__aenter__.return_value = mock_instance
    mock_instance.post.return_value.status_code = 204

    # Use valid UUID
    payload = {
        "installation_id": "550e8400-e29b-41d4-a716-446655440000",
        "heatpump_model": "test-model",
        "version": "1.0",
        "data": [{"timestamp": 1234567890, "temp": 20.5}],
    }

    # Needs auth
    headers = {"Authorization": "Bearer test-token"}
    response = client.post("/api/v1/submit", json=payload, headers=headers)

    assert response.status_code == 200

    # Check if post was called
    mock_instance.post.assert_called()

    # Check Influx line protocol format
    args, kwargs = mock_instance.post.call_args
    assert "heatpump_metrics" in kwargs["data"]
    assert "temp=20.5" in kwargs["data"]


def test_submit_telemetry_invalid_uuid(client):
    payload = {
        "installation_id": "invalid-uuid",
        "heatpump_model": "test-model",
        "version": "1.0",
        "data": [],
    }
    headers = {"Authorization": "Bearer test-token"}
    response = client.post("/api/v1/submit", json=payload, headers=headers)
    # Pydantic validation error 422
    assert response.status_code == 422


def test_submit_telemetry_invalid_model(client):
    payload = {
        "installation_id": "550e8400-e29b-41d4-a716-446655440000",
        "heatpump_model": "test/model",  # / is not allowed
        "version": "1.0",
        "data": [],
    }
    headers = {"Authorization": "Bearer test-token"}
    response = client.post("/api/v1/submit", json=payload, headers=headers)
    # Pydantic validation error 422
    assert response.status_code == 422


def test_submit_telemetry_unauthorized(client):
    response = client.post("/api/v1/submit", json={})
    assert response.status_code == 401


@patch("app.httpx.AsyncClient")
def test_pool_status(mock_client_cls, client):
    # Mock VM query responses
    mock_instance = AsyncMock()
    mock_client_cls.return_value.__aenter__.return_value = mock_instance

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "success",
        "data": {"result": [{"value": [123456, "20000"]}]},  # Adequate data points
    }
    mock_instance.get.return_value = mock_response

    response = client.get("/api/v1/pool/status")
    assert response.status_code == 200
    data = response.json()
    assert "total_installations" in data
    assert "total_data_points" in data


@patch("app.httpx.AsyncClient")
def test_check_eligibility_invalid_uuid(mock_client_cls, client):
    response = client.get("/api/v1/model/check?installation_id=invalid")
    assert response.status_code == 400
    assert "UUID" in response.json()["detail"]


@patch("app.httpx.AsyncClient")
def test_check_eligibility_invalid_model(mock_client_cls, client):
    # Valid UUID
    uuid_str = "550e8400-e29b-41d4-a716-446655440000"
    response = client.get(
        f"/api/v1/model/check?installation_id={uuid_str}&model=foo/bar"
    )
    assert response.status_code == 400
    assert "format" in response.json()["detail"]


@patch("app.httpx.AsyncClient")
def test_check_eligibility_valid_model_with_parens(mock_client_cls, client):
    # Valid UUID and model with parens
    uuid_str = "550e8400-e29b-41d4-a716-446655440000"

    # Mock VM response for eligibility
    mock_instance = AsyncMock()
    mock_client_cls.return_value.__aenter__.return_value = mock_instance

    mock_response = MagicMock()
    mock_response.status_code = 200
    # Return 20000 to satisfy data points check
    mock_response.json.return_value = {
        "status": "success",
        "data": {"result": [{"value": [123456, "20000"]}]},
    }
    mock_instance.get.return_value = mock_response

    response = client.get(
        f"/api/v1/model/check?installation_id={uuid_str}&model=AERO_SLM(v2)"
    )
    assert response.status_code == 200
    assert response.json()["eligible"] is True


@patch("app.get_community_averages")
def test_community_averages_endpoint(mock_analysis, client):
    mock_analysis.return_value = {
        "model": "AERO_SLM",
        "sample_size": 10,
        "metrics": {"cop_current": {"avg": 4.5}},
    }

    headers = {"Authorization": "Bearer test-token"}
    response = client.get(
        "/api/v1/community/averages?model=AERO_SLM&metrics=cop_current", headers=headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["sample_size"] == 10
    assert data["metrics"]["cop_current"]["avg"] == 4.5


def test_community_averages_invalid_metric(client):
    headers = {"Authorization": "Bearer test-token"}
    response = client.get(
        "/api/v1/community/averages?model=AERO_SLM&metrics=cop;drop", headers=headers
    )
    assert response.status_code == 400


@patch("app.httpx.AsyncClient")
def test_check_eligibility_admin_success(mock_client_cls, client):
    """Verify Admin ID is correctly identified and returns is_admin: True."""
    # Setup VM mock
    mock_instance = AsyncMock()
    mock_client_cls.return_value.__aenter__.return_value = mock_instance
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "success",
        "data": {"result": [{"value": [123456, "20000"]}]},
    }
    mock_instance.get.return_value = mock_response

    admin_uuid = "12345678-1234-1234-1234-123456789abc"

    # Patch ADMIN_IDS set with our test UUID
    with patch("app.ADMIN_IDS", {admin_uuid}):
        response = client.get(f"/api/v1/model/check?installation_id={admin_uuid}")
        assert response.status_code == 200
        data = response.json()
        assert data.get("is_admin") is True
        assert "server_stats" in data


@patch("app.httpx.AsyncClient")
def test_check_eligibility_admin_case_insensitive(mock_client_cls, client):
    """Verify Admin ID check is case insensitive."""
    # Setup VM mock
    mock_instance = AsyncMock()
    mock_client_cls.return_value.__aenter__.return_value = mock_instance
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "success",
        "data": {"result": [{"value": [123456, "20000"]}]},
    }
    mock_instance.get.return_value = mock_response

    admin_uuid_lower = "12345678-1234-1234-1234-123456789abc"
    admin_uuid_upper = admin_uuid_lower.upper()

    # Patch ADMIN_IDS set with LOWERCASE version
    with patch("app.ADMIN_IDS", {admin_uuid_lower}):
        # Request with UPPERCASE version
        response = client.get(f"/api/v1/model/check?installation_id={admin_uuid_upper}")
        assert response.status_code == 200
        data = response.json()
        assert data.get("is_admin") is True
