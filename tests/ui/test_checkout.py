"""
UI Test Suite: End-to-End Checkout Flow on SauceDemo.
"""

import pytest
from playwright.sync_api import Page, expect
from tests.ui.pages.login_page import LoginPage
from tests.ui.pages.inventory_page import InventoryPage
from tests.ui.pages.checkout_page import CheckoutPage


@pytest.mark.ui
@pytest.mark.smoke
def test_e2e_checkout_flow(page: Page):
    """
    End-to-End smoke test:
    1. Authenticate standard user
    2. Add item to cart
    3. Navigate to cart and start checkout
    4. Fill shipping information
    5. Finalize order and assert Thank You screen
    """
    # 1. Login
    login_page = LoginPage(page).open()
    login_page.login("standard_user", "secret_sauce")

    # 2. Add to cart
    inventory = InventoryPage(page)
    inventory.add_product_by_name("Sauce Labs Backpack")
    assert inventory.get_cart_count() == "1"
    inventory.go_to_cart()

    # 3. Checkout
    checkout = CheckoutPage(page)
    checkout.proceed_to_checkout()

    # 4. Shipping info
    checkout.fill_shipping_information(
        first_name="Candidate",
        last_name="Exceller",
        postal_code="560001"
    )

    # 5. Finish
    checkout.complete_order()
    header_text = checkout.get_confirmation_header()
    assert "Thank you for your order!" in header_text

