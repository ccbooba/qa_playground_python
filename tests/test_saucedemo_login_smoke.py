"""
SauceDemo login smoke tests.

TC-SMOKE-01: Valid login with standard_user.
TC-SMOKE-02: Locked user cannot log in.
TC-SMOKE-03: Invalid credentials cannot log in.
TC-SMOKE-04: Username only, password empty.
"""

from playwright.sync_api import Page, expect

LOGIN_URL = "https://www.saucedemo.com/"
VALID_USERNAME = "standard_user"
LOCKED_USERNAME = "locked_out_user"
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


def test_tc_smoke_02_locked_out_user_cannot_login(page: Page) -> None:
    # --- Arrange: open the login page ---
    page.goto(LOGIN_URL)

    username = page.locator('[data-test="username"]')
    password = page.locator('[data-test="password"]')
    login_button = page.locator('[data-test="login-button"]')

    # --- Act: attempt login with a locked account ---
    username.fill(LOCKED_USERNAME)
    password.fill(VALID_PASSWORD)
    login_button.click()

    # --- Assert: remain on login page with locked-out error ---
    expect(page).to_have_url(LOGIN_URL)
    expect(username).to_be_visible()
    expect(password).to_be_visible()

    error_banner = page.locator('[data-test="error"]')
    expect(error_banner).to_be_visible()
    expect(error_banner).to_contain_text("locked out")


def test_tc_smoke_03_invalid_credentials_cannot_login(page: Page) -> None:
    # --- Arrange: open the login page ---
    page.goto(LOGIN_URL)

    username = page.locator('[data-test="username"]')
    password = page.locator('[data-test="password"]')
    login_button = page.locator('[data-test="login-button"]')

    # --- Act: submit valid username with wrong password ---
    username.fill("standard_user")
    password.fill("wrong_password")
    login_button.click()

    # --- Assert: remain on login page with credentials mismatch error ---
    expect(page).to_have_url(LOGIN_URL)

    error_banner = page.locator('[data-test="error"]')
    expect(error_banner).to_be_visible()
    expect(error_banner).to_contain_text("Username and password do not match")


def test_tc_smoke_04_username_only_password_empty(page: Page) -> None:
    # --- Arrange: open the login page ---
    page.goto(LOGIN_URL)

    username = page.locator('[data-test="username"]')
    password = page.locator('[data-test="password"]')
    login_button = page.locator('[data-test="login-button"]')

    # --- Act: submit username only, leave password empty ---
    username.fill("standard_user")
    password.fill("")
    login_button.click()

    # --- Assert: remain on login page with password required error ---
    expect(page).to_have_url(LOGIN_URL)

    error_banner = page.locator('[data-test="error"]')
    expect(error_banner).to_be_visible()
    expect(error_banner).to_contain_text("Password is required")
