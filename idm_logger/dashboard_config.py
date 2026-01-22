# SPDX-License-Identifier: MIT
"""Dashboard configuration management."""

import uuid
import logging
from typing import Dict, List, Any, Optional
from .config import config

logger = logging.getLogger(__name__)


def get_default_dashboards() -> List[Dict[str, Any]]:
    """Get default dashboard configuration."""
    return [
        {
            "id": "default",
            "name": "Home Dashboard",
            "charts": [
                {
                    "id": str(uuid.uuid4()),
                    "title": "Underfloor Heating: Flow & Return Temp",
                    "queries": [
                        {
                            "label": "Flow Temp",
                            "query": "temp_flow_current_circuit_A",
                            "color": "#f59e0b",
                        },
                        {
                            "label": "Return Temp",
                            "query": "temp_return_circuit_A",
                            "color": "#3b82f6",
                        },
                        {
                            "label": "Heat Pump Power",
                            "query": "power_current_draw",
                            "color": "#ef4444",
                        },
                        {
                            "label": "Outdoor Temp",
                            "query": "temp_outside",
                            "color": "#22c55e",
                        },
                    ],
                    "hours": 12,
                },
                {
                    "id": str(uuid.uuid4()),
                    "title": "Tank Heating Sensing",
                    "queries": [
                        {
                            "label": "Buffer Tank Top",
                            "query": "temp_heat_storage",
                            "color": "#a855f7",
                        },
                        {
                            "label": "Buffer Tank Bottom",
                            "query": "temp_cold_storage",
                            "color": "#3b82f6",
                        },
                        {
                            "label": "Heat Pump Power",
                            "query": "power_current_draw",
                            "color": "#ef4444",
                        },
                    ],
                    "hours": 24,
                },
                {
                    "id": str(uuid.uuid4()),
                    "title": "Radiators Flow & Return: 1st & 2nd Floor",
                    "queries": [
                        {
                            "label": "Flow Temp",
                            "query": "temp_flow_current_circuit_B",
                            "color": "#f59e0b",
                        },
                        {
                            "label": "Return Temp",
                            "query": "temp_return_circuit_B",
                            "color": "#3b82f6",
                        },
                        {
                            "label": "Heat Pump Power",
                            "query": "power_current_draw",
                            "color": "#ef4444",
                        },
                        {
                            "label": "Outdoor Temp",
                            "query": "temp_outside",
                            "color": "#22c55e",
                        },
                    ],
                    "hours": 12,
                },
                {
                    "id": str(uuid.uuid4()),
                    "title": "3rd Floor: Flow & Return Temperatures",
                    "queries": [
                        {
                            "label": "Flow Temp",
                            "query": "temp_flow_current_circuit_C",
                            "color": "#f59e0b",
                        },
                        {
                            "label": "Return Temp",
                            "query": "temp_return_circuit_C",
                            "color": "#3b82f6",
                        },
                        {
                            "label": "Heat Pump Power",
                            "query": "power_current_draw",
                            "color": "#ef4444",
                        },
                        {
                            "label": "Outdoor Temp",
                            "query": "temp_outside",
                            "color": "#22c55e",
                        },
                    ],
                    "hours": 12,
                },
                {
                    "id": str(uuid.uuid4()),
                    "title": "3rd Floor Deep Dive",
                    "queries": [
                        {
                            "label": "Flow Temp",
                            "query": "temp_flow_current_circuit_C",
                            "color": "#f59e0b",
                        },
                        {
                            "label": "Return Temp",
                            "query": "temp_return_circuit_C",
                            "color": "#3b82f6",
                        },
                        {
                            "label": "Indoor Temp",
                            "query": "temp_room_circuit_C",
                            "color": "#a855f7",
                        },
                        {
                            "label": "Outdoor Temp",
                            "query": "temp_outside",
                            "color": "#22c55e",
                        },
                    ],
                    "hours": 12,
                },
                {
                    "id": str(uuid.uuid4()),
                    "title": "Consumption change",
                    "queries": [
                        {
                            "label": "Building Total",
                            "query": "power_current",
                            "color": "#3b82f6",
                        },
                        {
                            "label": "Heat Pump Total",
                            "query": "power_current_draw",
                            "color": "#ef4444",
                        },
                        {
                            "label": "Outdoor Temp",
                            "query": "temp_outside",
                            "color": "#22c55e",
                        },
                    ],
                    "hours": 24,
                },
            ],
        }
    ]


class DashboardManager:
    """Manages dashboard configurations."""

    def __init__(self):
        """Initialize dashboard manager."""
        self._ensure_dashboards_key()

    def _ensure_dashboards_key(self):
        """Ensure dashboards key exists in config."""
        if "dashboards" not in config.data:
            config.data["dashboards"] = get_default_dashboards()
            config.save()

    def get_all_dashboards(self) -> List[Dict[str, Any]]:
        """Get all dashboards."""
        return config.data.get("dashboards", [])

    def get_dashboard(self, dashboard_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific dashboard by ID."""
        dashboards = self.get_all_dashboards()
        for dashboard in dashboards:
            if dashboard["id"] == dashboard_id:
                return dashboard
        return None

    def create_dashboard(self, name: str) -> Dict[str, Any]:
        """Create a new dashboard."""
        dashboards = self.get_all_dashboards()
        new_dashboard = {
            "id": str(uuid.uuid4()),
            "name": name,
            "charts": [],
        }
        dashboards.append(new_dashboard)
        config.data["dashboards"] = dashboards
        config.save()
        logger.info(f"Created dashboard: {name}")
        return new_dashboard

    def update_dashboard(
        self, dashboard_id: str, updates: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Update a dashboard."""
        dashboards = self.get_all_dashboards()
        for i, dashboard in enumerate(dashboards):
            if dashboard["id"] == dashboard_id:
                dashboards[i].update(updates)
                config.data["dashboards"] = dashboards
                config.save()
                logger.info(f"Updated dashboard: {dashboard_id}")
                return dashboards[i]
        return None

    def delete_dashboard(self, dashboard_id: str) -> bool:
        """Delete a dashboard."""
        dashboards = self.get_all_dashboards()
        if len(dashboards) <= 1:
            logger.warning("Cannot delete the last dashboard")
            return False

        dashboards = [d for d in dashboards if d["id"] != dashboard_id]
        config.data["dashboards"] = dashboards
        config.save()
        logger.info(f"Deleted dashboard: {dashboard_id}")
        return True

    def add_chart(
        self,
        dashboard_id: str,
        title: str,
        queries: List[Dict[str, str]],
        hours: int = 12,
    ) -> Optional[Dict[str, Any]]:
        """Add a chart to a dashboard."""
        dashboard = self.get_dashboard(dashboard_id)
        if not dashboard:
            return None

        new_chart = {
            "id": str(uuid.uuid4()),
            "title": title,
            "queries": queries,
            "hours": hours,
        }

        dashboard["charts"].append(new_chart)
        self.update_dashboard(dashboard_id, {"charts": dashboard["charts"]})
        return new_chart

    def update_chart(
        self, dashboard_id: str, chart_id: str, updates: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Update a chart in a dashboard."""
        dashboard = self.get_dashboard(dashboard_id)
        if not dashboard:
            return None

        for i, chart in enumerate(dashboard["charts"]):
            if chart["id"] == chart_id:
                dashboard["charts"][i].update(updates)
                self.update_dashboard(dashboard_id, {"charts": dashboard["charts"]})
                return dashboard["charts"][i]
        return None

    def delete_chart(self, dashboard_id: str, chart_id: str) -> bool:
        """Delete a chart from a dashboard."""
        dashboard = self.get_dashboard(dashboard_id)
        if not dashboard:
            return False

        charts = [c for c in dashboard["charts"] if c["id"] != chart_id]
        if len(charts) == len(dashboard["charts"]):
            return False

        self.update_dashboard(dashboard_id, {"charts": charts})
        return True


# Global instance
dashboard_manager = DashboardManager()
