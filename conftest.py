"""
Root Pytest Fixtures and Configuration for the entire test suite.
Provides:
- In-memory/local Flask background test server accessible to both tests/ and ai_engine/generated/
- Database teardown/setup helpers
- HTML report customization with execution metadata
"""

import os
import sys
import time
import threading
import sqlite3
import pytest

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.sample_api.app import app as flask_app
from data.seed_data import init_database, get_db

TEST_API_HOST = "127.0.0.1"
TEST_API_PORT = 5055
BASE_API_URL = f"http://{TEST_API_HOST}:{TEST_API_PORT}"


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Ensure database is seeded before running any tests."""
    init_database()
    yield


@pytest.fixture(scope="session")
def api_server():
    """Starts the Flask sample API in a background thread for API tests."""
    server = threading.Thread(
        target=lambda: flask_app.run(host=TEST_API_HOST, port=TEST_API_PORT, debug=False, use_reloader=False),
        daemon=True
    )
    server.start()
    # Wait briefly for server startup
    time.sleep(1.0)
    yield BASE_API_URL


@pytest.fixture
def db_connection():
    """Provides a fresh database connection for a test."""
    conn = get_db()
    yield conn
    conn.close()


@pytest.fixture
def admin_auth_header():
    """Returns admin bearer token header."""
    return {"Authorization": "Bearer admin-token-xyz"}


@pytest.fixture
def customer_auth_header():
    """Returns customer bearer token header."""
    return {"Authorization": "Bearer standard-token-abc"}


# --- Pytest HTML Report Customization ---

def pytest_html_report_title(report):
    report.title = "Capgemini Quality Engineering - AI Test Automation Report"


def pytest_configure(config):
    """Add Capgemini Exceller SDET metadata to HTML report."""
    if hasattr(config, "_metadata"):
        config._metadata["Project"] = "AI-Augmented QA Framework"
        config._metadata["Role"] = "Test Automation / SDET / AI Engineer"
        config._metadata["Organization"] = "Capgemini Exceller Program"
        config._metadata["Tech Stack"] = "Python, Pytest, Playwright, Requests, Gemini AI, SQLite"
