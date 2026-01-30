import time
from playwright.sync_api import sync_playwright, expect

def test_alarms(page):
    print("Setting up routes...")
    # Mock API responses
    page.route("**/api/auth/check", lambda route: route.fulfill(json={"authenticated": True}))
    page.route("**/api/variables", lambda route: route.fulfill(json=[]))
    page.route("**/api/dashboards", lambda route: route.fulfill(json=[{"id": "d1", "name": "Test Dashboard", "charts": []}]))

    # Mock annotations with an anomaly
    anomaly = {
        "id": "1",
        "time": time.time(),
        "text": "Critical Anomaly Detected!",
        "tags": ["ai", "anomaly"],
        "color": "#ef4444",
        "dashboard_id": None,
        "acknowledged": False
    }

    def handle_annotations(route):
        print(f"Handling {route.request.method} {route.request.url}")
        if route.request.method == "GET":
            route.fulfill(json=[anomaly])
        else:
            route.continue_()

    page.route("**/api/annotations", handle_annotations)

    # Mock acknowledge endpoint
    def handle_acknowledge(route):
        print(f"Handling {route.request.method} {route.request.url}")
        if route.request.method == "PUT":
            route.fulfill(json={"id": "1", "acknowledged": True})
        else:
            route.continue_()

    page.route("**/api/annotations/1", handle_acknowledge)

    print("Navigating...")
    # Go to dashboard
    page.goto("http://localhost:4173/static/#/")

    print("Waiting for popup...")
    # Wait for Popup
    expect(page.get_by_text("Aktive Warnungen")).to_be_visible()
    expect(page.get_by_text("Critical Anomaly Detected!")).to_be_visible()

    print("Taking screenshot 1...")
    # Screenshot 1: Popup visible
    page.screenshot(path="/home/jules/verification/alarm_popup.png")

    print("Clicking Quittieren...")
    # Click Quittieren
    page.get_by_role("button", name="Quittieren").click()

    print("Waiting for popup to close...")
    # Verify popup closes or list empties
    # Since there was only 1, popup should close
    expect(page.get_by_text("Aktive Warnungen")).not_to_be_visible()

    print("Taking screenshot 2...")
    # Screenshot 2: Closed
    page.screenshot(path="/home/jules/verification/alarm_acknowledged.png")

if __name__ == "__main__":
    import os
    os.makedirs("/home/jules/verification", exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            test_alarms(page)
            print("Verification script ran successfully.")
        except Exception as e:
            print(f"Verification failed: {e}")
            page.screenshot(path="/home/jules/verification/failure.png")
            raise e
        finally:
            browser.close()
