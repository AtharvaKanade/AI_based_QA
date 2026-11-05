"""
Page Object representing the SauceDemo Cart and Checkout Flow.
"""

from playwright.sync_api import Page, expect
from tests.ui.pages.base_page import BasePage


class CheckoutPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.checkout_button = page.locator("#checkout")
        self.first_name_input = page.locator("#first-name")
        self.last_name_input = page.locator("#last-name")
        self.postal_code_input = page.locator("#postal-code")
        self.continue_button = page.locator("#continue")
        self.finish_button = page.locator("#finish")
        self.complete_header = page.locator(".complete-header")

    def proceed_to_checkout(self):
        self.checkout_button.click()

    def fill_shipping_information(self, first_name: str, last_name: str, postal_code: str):
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)
        self.continue_button.click()

    def complete_order(self):
        self.finish_button.click()

    def get_confirmation_header(self) -> str:
        expect(self.complete_header).to_be_visible()
        return self.complete_header.inner_text()

