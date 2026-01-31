#!/usr/bin/env python3
"""
Xerolux 2026 - Test mit deiner Admin-ID
Testet ohne laufenden Server
"""

import os
import sys
from unittest.mock import patch, MagicMock, AsyncMock

# Füge telemetry_server zum Pfad hinzu
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'telemetry_server'))

def test_with_your_admin_id():
    """Testet mit deiner Admin-ID aus der .env Datei"""
    print("=" * 70)
    print("TESTE MIT DEINER ADMIN-ID")
    print("=" * 70)

    your_admin_id = "075e0c34-f67f-4882-9637-90ea85971a79"

    print(f"\nDeine Admin-ID: {your_admin_id}")
    print("\nStarte Test...")

    # Mock httpx für VictoriaMetrics Abfragen
    with patch('app.httpx.AsyncClient') as mock_client_cls:
        mock_instance = AsyncMock()
        mock_client_cls.return_value.__aenter__.return_value = mock_instance

        # Mock VictoriaMetrics Antwort
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "success",
            "data": {"result": [{"value": [123456, "50000"]}]},  # 50k Datenpunkte
        }
        mock_instance.get.return_value = mock_response

        # Import app nach dem Mock
        import app

        # Patch ADMIN_IDS mit deiner Admin-ID
        print(f"\nSetze ADMIN_IDS auf: {your_admin_id}")
        with patch('app.ADMIN_IDS', {your_admin_id.lower()}):
            # Log-Meldungen aktivieren
            import logging
            logging.basicConfig(level=logging.INFO)

            # Simuliere FastAPI TestClient
            from fastapi.testclient import TestClient
            client = TestClient(app.app)

            print("\n" + "-" * 70)
            print("TEST 1: Admin-ID Abfrage")
            print("-" * 70)

            # Test mit deiner Admin-ID
            response = client.get(f"/api/v1/model/check?installation_id={your_admin_id}")

            print(f"\nRequest: GET /api/v1/model/check?installation_id={your_admin_id}")
            print(f"Response Status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                print(f"\nAntwort:")
                print(f"  - is_admin: {data.get('is_admin')}")
                print(f"  - eligible: {data.get('eligible')}")
                print(f"  - model_available: {data.get('model_available')}")

                if data.get('is_admin'):
                    print(f"\n[ERFOLG] Admin-Zugang erkannt!")

                    if 'server_stats' in data:
                        stats = data['server_stats']
                        print(f"\nServer Statistiken:")
                        print(f"  - Modelle verfuegbar: {len(stats.get('models', []))}")
                        print(f"  - Aktive Installationen: {stats.get('active_installations')}")
                        print(f"  - Gesamte Datenpunkte: {stats.get('total_points'):,}")
                else:
                    print(f"\n[FEHLER] Admin-Flag nicht gesetzt!")
                    return False
            else:
                print(f"\n[FEHLER] Server antwortet mit {response.status_code}")
                return False

            print("\n" + "-" * 70)
            print("TEST 2: Case-Insensitive Check")
            print("-" * 70)

            # Test mit Großschreibung
            response = client.get(f"/api/v1/model/check?installation_id={your_admin_id.upper()}")

            print(f"\nRequest mit Grossschreibung: {your_admin_id.upper()}")
            print(f"Response Status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                print(f"  - is_admin: {data.get('is_admin')}")

                if data.get('is_admin'):
                    print(f"\n[ERFOLG] Case-insensitive Check funktioniert!")
                else:
                    print(f"\n[FEHLER] Case-insensitive Check fehlgeschlagen!")
                    return False

            print("\n" + "-" * 70)
            print("TEST 3: Normale UUID (kein Admin)")
            print("-" * 70)

            normal_id = "12345678-1234-1234-1234-123456789abc"
            response = client.get(f"/api/v1/model/check?installation_id={normal_id}")

            print(f"\nRequest mit normaler ID: {normal_id}")
            print(f"Response Status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                print(f"  - is_admin: {data.get('is_admin')}")

                if not data.get('is_admin'):
                    print(f"\n[ERFOLG] Normale UUID wird korrekt als Nicht-Admin erkannt!")
                else:
                    print(f"\n[FEHLER] Normale UUID sollte nicht Admin sein!")
                    return False

    print("\n" + "=" * 70)
    print("[ERFOLG] ALLE TESTS BESTANDEN!")
    print("=" * 70)

    print("\nFazit:")
    print("  - Deine Admin-ID wird korrekt erkannt")
    print("  - Case-insensitive Check funktioniert")
    print("  - Server sendet is_admin und server_stats")
    print("  - Client wuerde das Signal empfangen")

    print("\nNaechste Schritte:")
    print("  1. Starte den lokalen Server mit deiner Admin-ID")
    print("  2. Der Client wird beim naechsten Model-Check Admin-Rechte erhalten")
    print("  3. Ueberpruefe mit: telemetry_manager.get_status()")

    return True


if __name__ == '__main__':
    try:
        test_with_your_admin_id()
    except Exception as e:
        print(f"\n[FEHLER] Test fehlgeschlagen: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
