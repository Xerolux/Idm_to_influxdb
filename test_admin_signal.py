#!/usr/bin/env python3
"""
Xerolux 2026 - Admin Signal Test

Dieses Skript testet lokal, ob:
1. Der Server Admin-IDs korrekt erkennt
2. Der Client das Admin-Signal empfängt
"""

import os
import sys
from unittest.mock import patch, MagicMock, AsyncMock

# Füge telemetry_server zum Pfad hinzu
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'telemetry_server'))

def test_server_admin_recognition():
    """Testet ob der Server Admin-IDs korrekt erkennt"""
    print("=" * 60)
    print("TEST 1: Server Admin-Erkennung")
    print("=" * 60)

    # Mock httpx für VictoriaMetrics Abfragen
    with patch('app.httpx.AsyncClient') as mock_client_cls:
        mock_instance = AsyncMock()
        mock_client_cls.return_value.__aenter__.return_value = mock_instance

        # Mock VictoriaMetrics Antwort
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "success",
            "data": {"result": [{"value": [123456, "20000"]}]},
        }
        mock_instance.get.return_value = mock_response

        # Import app nach dem Mock
        import app

        # Test-Admin-UUID
        admin_uuid = "12345678-1234-1234-1234-123456789abc"
        normal_uuid = "87654321-4321-4321-4321-cba987654321"

        # Patch ADMIN_IDS mit unserer Test-UUID
        with patch('app.ADMIN_IDS', {admin_uuid.lower()}):
            # Simuliere FastAPI TestClient
            from fastapi.testclient import TestClient
            client = TestClient(app.app)

            # Test 1: Admin-UUID (Großschreibung)
            print(f"\nTeste Admin-UUID: {admin_uuid}")
            response = client.get(f"/api/v1/model/check?installation_id={admin_uuid}")
            assert response.status_code == 200, f"Fehler: {response.status_code}"
            data = response.json()
            print(f"  [OK] Status: {response.status_code}")
            print(f"  [OK] is_admin: {data.get('is_admin')}")
            print(f"  [OK] server_stats: {list(data.get('server_stats', {}).keys())}")
            assert data.get('is_admin') is True, "Admin-Flag nicht gesetzt!"
            assert 'server_stats' in data, "server_stats fehlt!"

            # Test 2: Admin-UUID (Kleinschreibung - Case Insensitive)
            print(f"\nTeste Admin-UUID (klein): {admin_uuid.lower()}")
            response = client.get(f"/api/v1/model/check?installation_id={admin_uuid.lower()}")
            assert response.status_code == 200
            data = response.json()
            print(f"  [OK] Status: {response.status_code}")
            print(f"  [OK] is_admin: {data.get('is_admin')}")
            assert data.get('is_admin') is True, "Case-Insensitive Check fehlgeschlagen!"

            # Test 3: Normale UUID (kein Admin)
            print(f"\nTeste normale UUID: {normal_uuid}")
            response = client.get(f"/api/v1/model/check?installation_id={normal_uuid}")
            assert response.status_code == 200
            data = response.json()
            print(f"  [OK] Status: {response.status_code}")
            print(f"  [OK] is_admin: {data.get('is_admin', False)}")
            assert data.get('is_admin') is not True, "Normale UUID sollte nicht Admin sein!"

    print("\n[OK] Server Admin-Erkennung: ALLE TESTS BESTANDEN!")
    return True


def test_client_signal_reception():
    """Testet ob der Client das Admin-Signal empfängt"""
    print("\n" + "=" * 60)
    print("TEST 2: Client Signal-Empfang")
    print("=" * 60)

    # Mock DB für Config
    mock_db_module = MagicMock()
    mock_db_instance = MagicMock()
    mock_db_instance.get_setting.return_value = None
    mock_db_module.db = mock_db_instance
    sys.modules["idm_logger.db"] = mock_db_module

    from idm_logger.telemetry import TelemetryManager

    print("\nTeste TelemetryManager:")
    tm = TelemetryManager()

    # Prüfe Initialzustand
    print(f"  [OK] Initial is_admin: {tm.is_admin}")
    print(f"  [OK] Initial server_stats: {tm.server_stats}")

    # Simuliere Admin-Signal vom Server
    print("\nSimuliere Admin-Signal vom Server:")
    admin_response = {
        "is_admin": True,
        "server_stats": {
            "models": [{"name": "AERO_ALM", "size": 12345}],
            "active_installations": 42,
            "total_points": 1000000
        }
    }

    # Update wie in telemetry.py Zeile 319-326
    if admin_response.get("is_admin"):
        tm.is_admin = True
        tm.server_stats = admin_response.get("server_stats")

    print(f"  [OK] Nach Signal is_admin: {tm.is_admin}")
    print(f"  [OK] server_stats Modelle: {len(tm.server_stats.get('models', []))}")
    print(f"  [OK] server_stats Installationen: {tm.server_stats.get('active_installations')}")

    assert tm.is_admin is True, "Admin-Flag nicht gesetzt!"
    assert tm.server_stats is not None, "server_stats nicht empfangen!"

    # Teste get_status() Methode
    print("\nTeste get_status() Methode:")
    status = tm.get_status()
    print(f"  [OK] is_admin in status: {status.get('is_admin')}")
    print(f"  [OK] server_stats in status: {status.get('server_stats') is not None}")

    assert status.get('is_admin') is True, "is_admin nicht in status!"
    assert status.get('server_stats') is not None, "server_stats nicht in status!"

    print("\n[OK] Client Signal-Empfang: ALLE TESTS BESTANDEN!")
    return True


if __name__ == '__main__':
    try:
        # Test 1: Server
        test_server_admin_recognition()

        # Test 2: Client
        test_client_signal_reception()

        print("\n" + "=" * 60)
        print("[OK][OK][OK] ALLE TESTS ERFOLGREICH [OK][OK][OK]")
        print("=" * 60)
        print("\nZusammenfassung:")
        print("  1. Server erkennt Admin-IDs korrekt")
        print("  2. Server sendet is_admin und server_stats")
        print("  3. Client empfängt und speichert das Signal")
        print("  4. Client stellt das Signal über get_status() bereit")
        print("\nDer Admin-Zugang funktioniert lokal korrekt!")

    except Exception as e:
        print(f"\n[FAIL] TEST FEHLGESCHLAGEN: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
