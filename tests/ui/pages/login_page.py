"""
Page Object representing the SauceDemo Login Page.
"""

from playwright.sync_api import Page, expect
from tests.ui.pages.base_page import BasePage


class LoginPage(BasePage):
    URL = "https://www.saucedemo.com/"

    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_message = page.locator("[data-test='error']")

    def open(self):
        self.navigate_to(self.URL)
        return self

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def get_error_text(self) -> str:
        expect(self.error_message).to_be_visible()
        return self.error_message.inner_text()

