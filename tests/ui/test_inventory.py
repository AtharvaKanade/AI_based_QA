"""
UI Test Suite: Product Catalog and Cart Operations on SauceDemo.
"""

import pytest
from playwright.sync_api import Page, expect
from tests.ui.pages.login_page import LoginPage
from tests.ui.pages.inventory_page import InventoryPage


@pytest.fixture(autouse=True)
def logged_in_session(page: Page):
    """Fixture to ensure user is logged in before each inventory test."""
    login_page = LoginPage(page).open()
    login_page.login("standard_user", "secret_sauce")
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")


@pytest.mark.ui
@pytest.mark.smoke
def test_inventory_displays_products(page: Page):
    """Verify catalog displays all 6 expected standard items."""
    inventory = InventoryPage(page)
    assert inventory.get_items_count() == 6


@pytest.mark.ui
def test_add_product_to_cart_increments_badge(page: Page):
    """Verify adding item to cart reflects correctly on the shopping cart badge."""
    inventory = InventoryPage(page)
    inventory.add_first_product_to_cart()
    assert inventory.get_cart_count() == "1"


@pytest.mark.ui
def test_sort_products_low_to_high(page: Page):
    """Verify product sorting by Price (low to high)."""
    inventory = InventoryPage(page)
    inventory.sort_by("lohi")

    # Extract all prices and verify ascending order
    price_elements = page.locator(".inventory_item_price").all_inner_texts()
    prices = [float(p.replace("$", "")) for p in price_elements]
    assert prices == sorted(prices), f"Prices not sorted ascending: {prices}"


@pytest.mark.ui
def test_user_logout_flow(page: Page):
    """Verify user can log out via sidebar navigation."""
    inventory = InventoryPage(page)
    inventory.logout()
    expect(page).to_have_url("https://www.saucedemo.com/")

