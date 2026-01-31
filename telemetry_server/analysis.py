# Xerolux 2026
import os
import logging
import requests
from typing import List, Dict, Any, Optional
import httpx

logger = logging.getLogger("telemetry-analysis")

VM_QUERY_URL = os.environ.get(
    "VM_QUERY_URL", "http://victoriametrics:8428/api/v1/query"
)
VM_TIMEOUT = int(os.environ.get("VM_TIMEOUT", "5"))  # Configurable timeout in seconds


def get_community_averages(
    model_name: str,
    metrics: List[str],
    window: str = "24h",
    client: Optional[httpx.AsyncClient] = None
) -> Dict[str, Any]:
    """
    Fetch aggregated community statistics for a specific heat pump model.

    Args:
        model_name: The heat pump model name (e.g., 'AERO_SLM').
        metrics: List of metric suffixes to query (e.g., ['cop_current', 'temp_outdoor']).
        window: Time window for aggregation (default: '24h').
        client: Optional HTTPX client for async requests (uses requests if None).

    Returns:
        Dict containing averages, min, max, and sample size.
    """
    safe_model = model_name.replace(" ", "_")
    results = {"model": model_name, "window": window, "metrics": {}, "sample_size": 0}

    try:
        # Use synchronous requests for backward compatibility
        # If async client is provided in the future, we can switch to async mode

        # 1. Get sample size (approximate number of active installations for this model in window)
        count_query = f'count(count by (installation_id) (count_over_time({{__name__=~"heatpump_metrics_.*", model="{safe_model}"}}[{window}])))'

        response = requests.get(VM_QUERY_URL, params={"query": count_query}, timeout=VM_TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success" and data["data"]["result"]:
                results["sample_size"] = int(data["data"]["result"][0]["value"][1])

        # If no data, return early
        if results["sample_size"] == 0:
            return results

        # 2. Get stats for each metric
        for metric in metrics:
            metric_name = (
                f"heatpump_metrics_{metric}"
                if not metric.startswith("heatpump_metrics_")
                else metric
            )
            clean_name = metric.replace("heatpump_metrics_", "")

            queries = {
                "avg": f'avg(avg_over_time({metric_name}{{model="{safe_model}"}}[{window}]))',
                "min": f'min(min_over_time({metric_name}{{model="{safe_model}"}}[{window}]))',
                "max": f'max(max_over_time({metric_name}{{model="{safe_model}"}}[{window}]))',
            }

            metric_stats = {}
            for stat_type, query in queries.items():
                try:
                    res = requests.get(VM_QUERY_URL, params={"query": query}, timeout=VM_TIMEOUT)
                    if res.status_code == 200:
                        d = res.json()
                        if d.get("status") == "success" and d["data"]["result"]:
                            val = float(d["data"]["result"][0]["value"][1])
                            metric_stats[stat_type] = round(val, 2)
                except Exception as e:
                    logger.warning("metric_fetch_failed", metric=metric, stat=stat_type, error=str(e))

            if metric_stats:
                results["metrics"][clean_name] = metric_stats

    except Exception as e:
        logger.error("community_analysis_error", model=model_name, error=str(e))
        return {"error": str(e)}

    return results
