"""
Re-export root fixtures for tests/ directory compatibility.
"""
from conftest import (
    api_server,
    db_connection,
    admin_auth_header,
    customer_auth_header,
    setup_test_environment,
    pytest_html_report_title,
    pytest_configure
)
