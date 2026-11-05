"""
API Test Suite: Products Catalog and CRUD Operations.
Demonstrates:
- REST API contract validation
- Authorization boundary checks (RBAC)
- Query parameter filtering
- Creation, retrieval, and deletion lifecycle testing
"""

import pytest
import requests
from data.seed_data import fetch_products_by_category


@pytest.mark.api
@pytest.mark.smoke
def test_get_all_products(api_server):
    """Verify endpoint lists all products with expected schema."""
    response = requests.get(f"{api_server}/api/v1/products")
    assert response.status_code == 200
    data = response.json()
    assert "count" in data
    assert "products" in data
    assert data["count"] >= 5
    first = data["products"][0]
    for key in ["id", "name", "category", "price", "stock"]:
        assert key in first


@pytest.mark.api
def test_filter_products_by_category(api_server):
    """Verify category filtering matches database expectations."""
    db_apparel = fetch_products_by_category("apparel")
    response = requests.get(f"{api_server}/api/v1/products?category=apparel")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == len(db_apparel)
    for prod in data["products"]:
        assert prod["category"] == "apparel"


@pytest.mark.api
def test_filter_products_by_max_price(api_server):
    """Verify max_price query parameter boundary constraint."""
    max_threshold = 20.00
    response = requests.get(f"{api_server}/api/v1/products?max_price={max_threshold}")
    assert response.status_code == 200
    for prod in response.json()["products"]:
        assert prod["price"] <= max_threshold


@pytest.mark.api
def test_get_product_by_valid_id(api_server):
    """Verify fetching single product by existing ID returns product details."""
    response = requests.get(f"{api_server}/api/v1/products/1")
    assert response.status_code == 200
    product = response.json()
    assert product["id"] == 1
    assert "name" in product


@pytest.mark.api
def test_get_product_by_invalid_id_returns_404(api_server):
    """Verify nonexistent product ID returns HTTP 404."""
    response = requests.get(f"{api_server}/api/v1/products/99999")
    assert response.status_code == 404
    assert "error" in response.json()


@pytest.mark.api
def test_create_product_admin_success(api_server, admin_auth_header):
    """Verify admin user can successfully create a new product."""
    new_product = {
        "name": "Capgemini Quality Engineering Mug",
        "category": "swag",
        "price": 12.50,
        "stock": 50
    }
    response = requests.post(f"{api_server}/api/v1/products", json=new_product, headers=admin_auth_header)
    assert response.status_code == 201
    res_data = response.json()
    assert "product_id" in res_data
    created_id = res_data["product_id"]

    # Verify newly created product is retrievable
    get_res = requests.get(f"{api_server}/api/v1/products/{created_id}")
    assert get_res.status_code == 200
    assert get_res.json()["name"] == new_product["name"]

    # Cleanup: Delete product
    del_res = requests.delete(f"{api_server}/api/v1/products/{created_id}", headers=admin_auth_header)
    assert del_res.status_code == 200


@pytest.mark.api
def test_create_product_forbidden_for_standard_user(api_server, customer_auth_header):
    """Verify non-admin users cannot create products (RBAC enforcement)."""
    payload = {"name": "Unauthorized Item", "category": "test", "price": 10.0}
    response = requests.post(f"{api_server}/api/v1/products", json=payload, headers=customer_auth_header)
    assert response.status_code == 403
    assert "Unauthorized" in response.json()["error"]


@pytest.mark.api
def test_create_product_validation_error(api_server, admin_auth_header):
    """Verify invalid payloads (negative price) return 400 Bad Request."""
    invalid_payload = {"name": "Bad Product", "price": -5.0}
    response = requests.post(f"{api_server}/api/v1/products", json=invalid_payload, headers=admin_auth_header)
    assert response.status_code == 400
    assert "error" in response.json()

