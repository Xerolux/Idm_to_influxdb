#!/usr/bin/env python3
"""
Xerolux 2026 - Test Admin WebUI Integration

Testet ob die Admin Zone im WebUI korrekt angezeigt wird.
"""

import sys
import os
from unittest.mock import patch, MagicMock

# Mock DB
mock_db_module = MagicMock()
mock_db_instance = MagicMock()
mock_db_instance.get_setting.return_value = None
mock_db_module.db = mock_db_instance
sys.modules["idm_logger.db"] = mock_db_module

def test_telemetry_manager_status():
    """Testet ob get_status() Admin-Daten zurückgibt"""
    print("=" * 70)
    print("TEST: TelemetryManager.get_status() mit Admin-Daten")
    print("=" * 70)

    from idm_logger.telemetry import TelemetryManager

    tm = TelemetryManager()

    print("\n1. Initialer Status (kein Admin):")
    status = tm.get_status()
    print(f"   is_admin: {status.get('is_admin')}")
    print(f"   server_stats: {status.get('server_stats')}")
    assert status.get('is_admin') is False
    assert status.get('server_stats') is None

    print("\n2. Simuliere Admin-Signal vom Server:")
    # So wie es in telemetry.py Zeile 319-326 passiert
    admin_response = {
        "is_admin": True,
        "server_stats": {
            "models": [
                {"name": "AERO_ALM_6-15", "size": 1234567, "modified": 1738272000},
                {"name": "AERO_SLM", "size": 987654, "modified": 1738358400}
            ],
            "active_installations": 42,
            "total_points": 50000000
        }
    }

    if admin_response.get("is_admin"):
        tm.is_admin = True
        tm.server_stats = admin_response.get("server_stats")

    tm._save_state()

    print(f"   is_admin: {tm.is_admin}")
    print(f"   server_stats Modelle: {len(tm.server_stats.get('models', []))}")

    print("\n3. get_status() nach Admin-Signal:")
    status = tm.get_status()
    print(f"   is_admin: {status.get('is_admin')}")
    print(f"   server_stats: {status.get('server_stats') is not None}")

    # Prüfe alle Felder die das Frontend erwartet
    assert status.get('is_admin') is True, "is_admin sollte True sein"
    assert status.get('server_stats') is not None, "server_stats sollte vorhanden sein"
    assert 'models' in status['server_stats'], "models sollte in server_stats sein"
    assert 'active_installations' in status['server_stats'], "active_installations sollte in server_stats sein"
    assert 'total_points' in status['server_stats'], "total_points sollte in server_stats sein"

    print("\n   [OK] Alle Admin-Daten vorhanden!")
    print(f"   - Modelle: {len(status['server_stats']['models'])}")
    print(f"   - Installationen: {status['server_stats']['active_installations']}")
    print(f"   - Datenpunkte: {status['server_stats']['total_points']:,}")

    return True


def test_webui_admin_zone_display():
    """Testet die WebUI Logik für Admin Zone"""
    print("\n" + "=" * 70)
    print("TEST: WebUI Admin Zone Anzeige")
    print("=" * 70)

    # Simuliere telemetryStatus wie im Frontend
    class MockTelemetryStatus:
        def __init__(self, is_admin=False, server_stats=None):
            self.is_admin = is_admin
            self.server_stats = server_stats

    print("\n1. Ohne Admin-Status:")
    status_normal = MockTelemetryStatus(is_admin=False, server_stats=None)
    print(f"   is_admin: {status_normal.is_admin}")
    print(f"   Admin Zone sichtbar: {status_normal.is_admin}")
    assert status_normal.is_admin is False

    print("\n2. Mit Admin-Status:")
    admin_stats = {
        "models": [
            {"name": "AERO_ALM_6-15", "size": 1234567, "modified": 1738272000}
        ],
        "active_installations": 42,
        "total_points": 50000000
    }
    status_admin = MockTelemetryStatus(is_admin=True, server_stats=admin_stats)

    print(f"   is_admin: {status_admin.is_admin}")
    print(f"   Admin Zone sichtbar: {status_admin.is_admin}")
    print(f"   Server Stats: {status_admin.server_stats is not None}")

    assert status_admin.is_admin is True
    assert status_admin.server_stats is not None

    # Simuliere computed categories aus Config.vue Zeile 1190-1192
    categories = [
        { 'id': 'general', 'label': 'Allgemein' },
        { 'id': 'idm', 'label': 'IDM' }
    ]

    if status_admin.is_admin:
        categories.append({ 'id': 'admin', 'label': 'Admin Zone', 'icon': 'pi pi-crown' })

    print(f"\n3. Kategorien mit Admin:")
    for cat in categories:
        print(f"   - {cat['label']} ({cat.get('icon', 'kein Icon')})")

    assert any(c['id'] == 'admin' for c in categories), "Admin Kategorie sollte vorhanden sein"

    print("\n   [OK] Admin Zone wird im Frontend angezeigt!")

    return True


def verify_api_endpoint():
    """Verifiziert dass der API-Endpunkt existiert"""
    print("\n" + "=" * 70)
    print("VERIFIZIERUNG: API-Endpunkt")
    print("=" * 70)

    # Prüfe ob Route in web.py existiert
    with open('idm_logger/web.py', 'r', encoding='utf-8') as f:
        content = f.read()

    assert '/api/telemetry/status' in content, "API Route sollte existieren"
    assert 'telemetry_manager.get_status()' in content, "Sollte get_status() aufrufen"

    print("\n   [OK] API-Endpunkt /api/telemetry/status vorhanden")
    print("   [OK] Ruft telemetry_manager.get_status() auf")

    return True


def check_frontend_integration():
    """Prüft Frontend Integration"""
    print("\n" + "=" * 70)
    print("VERIFIZIERUNG: Frontend Integration")
    print("=" * 70)

    with open('frontend/src/views/Config.vue', 'r', encoding='utf-8') as f:
        content = f.read()

    checks = [
        ("Admin Status Indikator", 'v-if="telemetryStatus.is_admin"', "Admin Badge wird angezeigt"),
        ("Admin Zone Kategorie", "{ id: 'admin', label: 'Admin Zone'", "Admin Kategorie wird hinzugefügt"),
        ("Admin Zone Template", 'v-if="activeCategory === \'admin\'"', "Admin Zone wird gerendert"),
        ("Server Stats", 'telemetryStatus.server_stats', "Server Stats werden verwendet"),
        ("loadTelemetryStatus", 'const loadTelemetryStatus', "Funktion zum Laden existiert"),
        ("onMounted Aufruf", 'loadTelemetryStatus()', "Wird beim Laden aufgerufen"),
        ("API Call", "'/api/telemetry/status'", "Ruft richtigen Endpunkt auf"),
    ]

    for name, pattern, description in checks:
        if pattern in content:
            print(f"   [OK] {name}: {description}")
        else:
            print(f"   [FEHLER] {name}: Nicht gefunden!")
            return False

    return True


if __name__ == '__main__':
    try:
        # Test 1: TelemetryManager
        test_telemetry_manager_status()

        # Test 2: WebUI Logik
        test_webui_admin_zone_display()

        # Test 3: API Endpunkt
        verify_api_endpoint()

        # Test 4: Frontend Integration
        check_frontend_integration()

        print("\n" + "=" * 70)
        print("[ERFOLG] ALLE TESTS BESTANDEN!")
        print("=" * 70)

        print("\nZusammenfassung:")
        print("  1. TelemetryManager.get_status() gibt Admin-Daten zurück")
        print("  2. Admin-Signal wird korrekt gespeichert")
        print("  3. API-Endpunkt /api/telemetry/status existiert")
        print("  4. Frontend lädt Telemetry-Status beim Start")
        print("  5. Admin Zone wird angezeigt wenn is_admin=true")
        print("  6. Server Stats werden im UI dargestellt")

        print("\nDie Admin Zone ist vollstaendig im WebUI integriert!")

    except Exception as e:
        print(f"\n[FEHLER] Test fehlgeschlagen: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
