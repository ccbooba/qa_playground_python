"""
TC-SMOKE-01: Valid login with standard_user (SauceDemo).

Test case: P-01 — confirm a valid user reaches the product inventory after login.
"""

from playwright.sync_api import Page, expect

LOGIN_URL = "https://www.saucedemo.com/"
VALID_USERNAME = "standard_user"
VALID_PASSWORD = "secret_sauce"


def test_tc_smoke_01_valid_login_standard_user(page: Page) -> None:
    # --- Arrange: open the login page ---
    page.goto(LOGIN_URL)

    # SauceDemo uses data-test (not data-testid); attribute selectors are stable here
    username = page.locator('[data-test="username"]')
    password = page.locator('[data-test="password"]')
    login_button = page.locator('[data-test="login-button"]')

    expect(username).to_be_visible()
    expect(password).to_be_visible()
    expect(login_button).to_be_enabled()

    # --- Act: submit valid credentials ---
    username.fill(VALID_USERNAME)
    password.fill(VALID_PASSWORD)
    login_button.click()

    # --- Assert: successful authentication and inventory page ---
    # URL confirms redirect away from login
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

    # Inventory container and at least one product — proves catalog loaded
    inventory = page.locator('[data-test="inventory-container"]')
    expect(inventory).to_be_visible()
    expect(inventory.locator('[data-test="inventory-item"]').first).to_be_visible()

    # Page heading matches authenticated inventory view
    expect(page.locator('[data-test="title"]')).to_have_text("Products")

    # No login error banner after successful sign-in
    expect(page.locator('[data-test="error"]')).to_have_count(0)
