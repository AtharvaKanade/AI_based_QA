"""
API Test Suite: Authentication and User Management.
Demonstrates:
- Parameterized testing with Pytest
- Data-driven testing sourcing credentials from SQLite DB
- Positive & negative assertions on HTTP status codes and JSON response schemas
"""

import pytest
import requests
from data.seed_data import fetch_test_users


@pytest.mark.api
@pytest.mark.smoke
def test_api_health_endpoint(api_server):
    """Verify system health endpoint returns 200 OK and valid schema."""
    response = requests.get(f"{api_server}/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "ecommerce-api"
    assert "version" in data


@pytest.mark.api
def test_successful_admin_login(api_server):
    """Verify valid admin user can authenticate and receives admin token."""
    payload = {
        "username": "admin_user",
        "password": "AdminPass123!"
    }
    response = requests.post(f"{api_server}/api/v1/auth/login", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert "token" in body
    assert body["token"] == "admin-token-xyz"
    assert body["user"]["role"] == "admin"


@pytest.mark.api
def test_login_locked_user_forbidden(api_server):
    """Verify locked users receive HTTP 403 Forbidden with appropriate error message."""
    payload = {
        "username": "locked_user",
        "password": "LockedPass123!"
    }
    response = requests.post(f"{api_server}/api/v1/auth/login", json=payload)
    assert response.status_code == 403
    body = response.json()
    assert "Account is locked" in body["error"]


@pytest.mark.api
@pytest.mark.parametrize("invalid_user,invalid_pass", [
    ("nonexistent_user", "wrongpassword"),
    ("admin_user", "WrongPassword!"),
    ("", "")
])
def test_login_invalid_credentials_rejected(api_server, invalid_user, invalid_pass):
    """Verify invalid credentials or empty payloads are rejected with 400 or 401."""
    payload = {"username": invalid_user, "password": invalid_pass}
    response = requests.post(f"{api_server}/api/v1/auth/login", json=payload)
    assert response.status_code in [400, 401]
    assert "error" in response.json()


@pytest.mark.api
def test_data_driven_login_validation(api_server):
    """
    Data-driven test pulling user fixtures directly from SQLite database.
    Demonstrates SQL integration in automated test execution.
    """
    users = fetch_test_users()
    assert len(users) > 0, "Database should contain seeded test users"

    for user in users:
        payload = {"username": user["username"], "password": user["password"]}
        response = requests.post(f"{api_server}/api/v1/auth/login", json=payload)

        if user["status"] == "locked":
            assert response.status_code == 403
        else:
            assert response.status_code == 200
            assert response.json()["user"]["role"] == user["role"]

