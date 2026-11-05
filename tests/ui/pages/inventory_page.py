"""
Page Object representing the SauceDemo Products/Inventory Page.
"""

from playwright.sync_api import Page, expect
from tests.ui.pages.base_page import BasePage


class InventoryPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.inventory_items = page.locator(".inventory_item")
        self.shopping_cart_badge = page.locator(".shopping_cart_badge")
        self.shopping_cart_link = page.locator(".shopping_cart_link")
        self.sort_select = page.locator("[data-test='product-sort-container']")
        self.menu_button = page.locator("#react-burger-menu-btn")
        self.logout_link = page.locator("#logout_sidebar_link")

    def wait_for_inventory_loaded(self):
        """Wait for inventory list to be visible in DOM."""
        expect(self.inventory_items.first).to_be_visible()

    def get_items_count(self) -> int:
        self.wait_for_inventory_loaded()
        return self.inventory_items.count()

    def add_first_product_to_cart(self):
        self.wait_for_inventory_loaded()
        self.inventory_items.first.locator("button").click()

    def add_product_by_name(self, product_name: str):
        self.wait_for_inventory_loaded()
        item = self.inventory_items.filter(has_text=product_name)
        item.locator("button").click()

    def get_cart_count(self) -> str:
        return self.shopping_cart_badge.inner_text()

    def sort_by(self, option_value: str):
        # Options: 'az' (A to Z), 'za' (Z to A), 'lohi' (low to high), 'hilo' (high to low)
        self.wait_for_inventory_loaded()
        self.sort_select.select_option(option_value)

    def go_to_cart(self):
        self.shopping_cart_link.click()

    def logout(self):
        self.menu_button.click()
        expect(self.logout_link).to_be_visible()
        self.logout_link.click()
