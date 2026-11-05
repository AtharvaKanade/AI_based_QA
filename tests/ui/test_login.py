"""
UI Test Suite: Authentication on SauceDemo.
Demonstrates:
- Page Object Model (POM) pattern
- Positive and Negative UI test cases
- Playwright sync API with robust locators and auto-waiting assertions
"""

import pytest
from playwright.sync_api import Page, expect
from tests.ui.pages.login_page import LoginPage


@pytest.mark.ui
@pytest.mark.smoke
def test_valid_user_login(page: Page):
    """Verify standard user can log in and navigates to inventory dashboard."""
    login_page = LoginPage(page).open()
    login_page.login("standard_user", "secret_sauce")

    # Assert navigation to inventory page
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    expect(page.locator(".title")).to_have_text("Products")


@pytest.mark.ui
def test_locked_out_user_error(page: Page):
    """Verify locked out user receives explicit error message."""
    login_page = LoginPage(page).open()
    login_page.login("locked_out_user", "secret_sauce")

    error_text = login_page.get_error_text()
    assert "Sorry, this user has been locked out" in error_text


@pytest.mark.ui
@pytest.mark.parametrize("user,pwd,expected_snippet", [
    ("", "", "Username is required"),
    ("standard_user", "", "Password is required"),
    ("invalid_user", "invalid_pass", "Username and password do not match")
])
def test_login_validation_errors(page: Page, user, pwd, expected_snippet):
    """Verify validation messages for missing/invalid credentials."""
    login_page = LoginPage(page).open()
    login_page.login(user, pwd)

    error_text = login_page.get_error_text()
    assert expected_snippet in error_text

