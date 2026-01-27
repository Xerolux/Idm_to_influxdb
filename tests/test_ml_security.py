# SPDX-License-Identifier: MIT
"""Tests for ML alert security functionality."""

import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Add repo root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import helpers from conftest
from conftest import create_mock_db_module, create_mock_config


@pytest.fixture(autouse=True)
def clean_modules():
    """Clean up idm_logger modules before and after each test."""
    for mod in list(sys.modules.keys()):
        if mod.startswith("idm_logger"):
            del sys.modules[mod]
    yield
    for mod in list(sys.modules.keys()):
        if mod.startswith("idm_logger"):
            del sys.modules[mod]


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    mock_db_module = create_mock_db_module()
    mock_config = create_mock_config()

    with patch.dict(
        sys.modules,
        {
            "idm_logger.db": mock_db_module,
            "idm_logger.mqtt": MagicMock(),
            "idm_logger.modbus": MagicMock(),
        },
    ):
        with patch("idm_logger.config.config", mock_config):
            from idm_logger.web import app

            app.config["TESTING"] = True
            app.secret_key = b"test-secret"

            # Store config reference
            app.test_mock_config = mock_config

            with app.test_client() as test_client:
                yield test_client, mock_config


def test_fail_closed_when_key_missing(client):
    """Test that the endpoint returns 503 when INTERNAL_API_KEY is not configured."""
    test_client, mock_config = client

    # Ensure no key is set
    mock_config.data["internal_api_key"] = None

    response = test_client.post("/api/internal/ml_alert", json={"score": 0.9})
    assert response.status_code == 503
    assert "Configuration Error" in response.get_json().get("error")


def test_fail_auth_when_key_set_but_header_missing(client):
    """Test that the endpoint returns 401 when key is set but header is missing."""
    test_client, mock_config = client

    # Set key
    mock_config.data["internal_api_key"] = "secure-key"

    response = test_client.post("/api/internal/ml_alert", json={"score": 0.9})
    assert response.status_code == 401
    assert "Unauthorized" in response.get_json().get("error")


def test_success_when_key_and_header_match(client):
    """Test that the endpoint returns success when key matches header."""
    test_client, mock_config = client

    # Set key
    mock_config.data["internal_api_key"] = "secure-key"

    with patch("idm_logger.web.notification_manager.send_all"):
        response = test_client.post(
            "/api/internal/ml_alert",
            json={"score": 0.9},
            headers={"X-Internal-Secret": "secure-key"},
        )
        assert response.status_code in [200, 201]
