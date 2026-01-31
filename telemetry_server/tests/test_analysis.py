# Xerolux 2026
from unittest.mock import MagicMock, AsyncMock
import sys
import os
import pytest
import httpx

# Ensure telemetry_server is in path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from analysis import get_community_averages


@pytest.mark.anyio
async def test_get_community_averages_success():
    # Mock Client
    mock_client = AsyncMock(spec=httpx.AsyncClient)

    # Mock responses for count, avg, min, max
    r1 = MagicMock()
    r1.status_code = 200
    r1.json.return_value = {
        "status": "success",
        "data": {"result": [{"value": [123456, "10"]}]},
    }

    r2 = MagicMock()
    r2.status_code = 200
    r2.json.return_value = {
        "status": "success",
        "data": {"result": [{"value": [123456, "4.2"]}]},
    }

    r3 = MagicMock()
    r3.status_code = 200
    r3.json.return_value = {
        "status": "success",
        "data": {"result": [{"value": [123456, "3.5"]}]},
    }

    async def mock_get(url, params=None, timeout=None):
        query = params.get("query", "")
        if "count(" in query:
            return r1
        elif "avg(" in query:
            return r2
        elif "min(" in query or "max(" in query:
            return r3
        return MagicMock(status_code=404)

    mock_client.get.side_effect = mock_get

    result = await get_community_averages(
        "AERO_SLM", ["cop_current"], client=mock_client
    )

    assert result["model"] == "AERO_SLM"
    assert result["sample_size"] == 10
    assert "metrics" in result
    assert "cop_current" in result["metrics"]
    assert result["metrics"]["cop_current"]["avg"] == 4.2
    assert result["metrics"]["cop_current"]["min"] == 3.5


@pytest.mark.anyio
async def test_get_community_averages_no_data():
    mock_client = AsyncMock(spec=httpx.AsyncClient)
    r1 = MagicMock()
    r1.status_code = 200
    r1.json.return_value = {
        "status": "success",
        "data": {"result": []},
    }
    mock_client.get.return_value = r1

    result = await get_community_averages(
        "Unknown", ["cop_current"], client=mock_client
    )
    assert result["sample_size"] == 0
    assert result["metrics"] == {}


@pytest.mark.anyio
async def test_get_community_averages_error():
    mock_client = AsyncMock(spec=httpx.AsyncClient)
    mock_client.get.side_effect = Exception("VM Down")

    result = await get_community_averages(
        "AERO_SLM", ["cop_current"], client=mock_client
    )
    assert "error" in result
