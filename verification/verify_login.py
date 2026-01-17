# SPDX-License-Identifier: MIT
import time
from playwright.sync_api import sync_playwright, expect

def verify_login_ux():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        print("Navigating to login page...")
        # Note: The app uses /static/ base
        page.goto("http://localhost:5173/static/login")

        print("Checking initial state...")
        # 1. Verify error message is NOT visible initially
        error_locator = page.locator(".text-error-400")
        if error_locator.count() > 0:
             print("Error locator found, checking visibility")
             # It might be in DOM but hidden or not in DOM.
             # In Vue v-if removes it from DOM.
             # Wait, my change uses v-if="showPasswordError"
             # So expect(error_locator).not_to_be_visible() should pass or to_have_count(0)
             if error_locator.is_visible():
                 print("FAIL: Error message is visible initially!")
                 page.screenshot(path="verification/fail_initial.png")
                 browser.close()
                 return
             else:
                 print("PASS: Error message not visible initially.")
        else:
             print("PASS: Error message not in DOM initially.")

        page.screenshot(path="verification/1_initial_state.png")

        # 2. Focus and Blur (touch)
        print("Interacting with password field...")
        password_input = page.locator("#password")
        password_input.click() # Focus
        page.locator("body").click() # Blur

        # Now error should be visible
        print("Checking error after blur...")
        expect(page.locator("text=Passwort ist erforderlich")).to_be_visible()
        page.screenshot(path="verification/2_after_blur.png")
        print("PASS: Error visible after blur.")

        # 3. Type something
        print("Typing password...")
        password_input.fill("test")
        # Error should disappear (because valid)
        expect(page.locator("text=Passwort ist erforderlich")).not_to_be_visible()
        print("PASS: Error gone after typing.")

        # 4. Clear input
        password_input.fill("")
        # Error should appear again
        expect(page.locator("text=Passwort ist erforderlich")).to_be_visible()
        print("PASS: Error reappears after clearing.")

        # 5. Refresh page and try Submit button immediately
        print("Refreshing page...")
        page.reload()

        # Click login
        print("Clicking login button...")
        # Note: Button is disabled if invalid?
        # My code: :disabled="!isValid"
        # isValid = password.value && !passwordError.value
        # Initially password is empty, so isValid is false.
        # So button IS disabled.

        login_button = page.locator("button", has_text="Login")
        if login_button.is_disabled():
            print("Login button is disabled initially. This is expected behavior for empty form.")
        else:
             print("FAIL: Login button is enabled initially?")

        # But I wanted to test that submitting shows error?
        # If button is disabled, I can't click it.
        # But if I press Enter in the field?

        password_input = page.locator("#password")
        password_input.focus()
        password_input.press("Enter")

        # Now touched should be true, and error visible?
        # @keyup.enter="handleLogin"
        # handleLogin sets touched=true.
        # But wait, handleLogin is only called if I press enter.
        # Let's check if error appears.

        expect(page.locator("text=Passwort ist erforderlich")).to_be_visible()
        print("PASS: Error visible after Enter key.")
        page.screenshot(path="verification/3_after_enter.png")

        browser.close()

if __name__ == "__main__":
    verify_login_ux()
