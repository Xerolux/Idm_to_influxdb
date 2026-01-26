from playwright.sync_api import sync_playwright
import time
import subprocess
import os
import signal
import sys

def verify_metric_row():
    # Start the backend server
    env = os.environ.copy()
    env["PYTHONPATH"] = os.getcwd()
    env["METRICS_URL"] = "http://localhost:9999" # Dummy
    env["ADMIN_PASSWORD"] = "password123" # Set known password

    server_process = subprocess.Popen(
        [sys.executable, "-m", "idm_logger"],
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    try:
        # Give it a moment to start
        time.sleep(5)

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # Mock API responses
            def handle_metrics_available(route):
                print("Intercepted /api/metrics/available")
                route.fulfill(json={
                    "temperature": [
                        {"name": "temp_outdoor", "display": "Außentemperatur"},
                        {"name": "temp_indoor", "display": "Innentemperatur"}
                    ],
                    "status": [
                        {"name": "status_heat_pump", "display": "Wärmepumpe Status"}
                    ]
                })

            def handle_data(route):
                print("Intercepted /api/data")
                route.fulfill(json={
                    "temp_outdoor": 12.5,
                    "temp_indoor": 22.0,
                    "status_heat_pump": 1
                })

            page.route("**/api/metrics/available", handle_metrics_available)
            page.route("**/api/data**", handle_data)

            # Navigate
            try:
                page.goto("http://localhost:5000", timeout=10000)
            except Exception as e:
                print(f"Failed to load page: {e}")
                raise

            # Check if we are on login page
            if page.locator("input[id='password']").is_visible():
                print("On Login Page. Logging in...")
                page.fill("input[id='password']", "password123")

                # Click Login button
                # PrimeVue button might be complex, try get_by_role
                try:
                    page.get_by_role("button", name="Login").click()
                except:
                    # Fallback
                    page.locator("button").filter(has_text="Login").click()

                # Wait for navigation
                page.wait_for_url("**/#/", timeout=5000)

            # Wait for content
            try:
                page.wait_for_selector(".space-y-3", state="visible", timeout=10000)
            except Exception as e:
                print("Timeout waiting for content. Taking screenshot.")
                page.screenshot(path="verification/failed.png")
                raise e

            rows = page.locator("[draggable='true']")
            count = rows.count()
            print(f"Found {count} metric rows")

            if count == 0:
                print("Error: No metric rows found!")
                page.screenshot(path="verification/failed.png")
                return False

            first_row = rows.first
            print(f"First row text: {first_row.inner_text()}")

            # 12.5 should be formatted to "12.5" and unit "°C"
            if "12.5" in first_row.inner_text() and "°C" in first_row.inner_text():
                print("Verification Passed: Value and Unit rendered correctly")
            else:
                print("Verification Failed: Value or Unit missing")

            page.screenshot(path="verification/verification.png")
            return True

    finally:
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    success = verify_metric_row()
    if not success:
        sys.exit(1)
