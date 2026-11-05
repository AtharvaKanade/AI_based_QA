"""
Database Seeding and Test Data Management Module.
Sets up SQLite schema and seeds deterministic test fixtures for testing.
"""

import sqlite3
import os

DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, "test_data.db")


def get_db():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """Create tables for users and products."""
    conn = get_db()
    cursor = conn.cursor()

    # Drop existing tables for fresh seed
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("DROP TABLE IF EXISTS products")

    cursor.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'active'
    )
    """)

    cursor.execute("""
    CREATE TABLE products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL,
        stock INTEGER NOT NULL DEFAULT 0
    )
    """)

    # Seed users
    users = [
        ("admin_user", "AdminPass123!", "admin", "active"),
        ("standard_user", "StandardPass123!", "customer", "active"),
        ("locked_user", "LockedPass123!", "customer", "locked"),
        ("performance_glitch_user", "SecretPass123!", "customer", "active")
    ]
    cursor.executemany(
        "INSERT INTO users (username, password, role, status) VALUES (?, ?, ?, ?)",
        users
    )

    # Seed products
    products = [
        ("Sauce Labs Backpack", "apparel", 29.99, 15),
        ("Sauce Labs Bike Light", "electronics", 9.99, 25),
        ("Sauce Labs Bolt T-Shirt", "apparel", 15.99, 40),
        ("Sauce Labs Fleece Jacket", "apparel", 49.99, 10),
        ("Sauce Labs Onesie", "apparel", 7.99, 30),
        ("Test.allTheThings() T-Shirt (Red)", "apparel", 15.99, 12)
    ]
    cursor.executemany(
        "INSERT INTO products (name, category, price, stock) VALUES (?, ?, ?, ?)",
        products
    )

    conn.commit()
    conn.close()
    print(f"[+] Test database seeded successfully at: {DB_PATH}")


def fetch_test_users():
    """Utility function to retrieve seeded users for data-driven tests."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT username, password, role, status FROM users")
    users = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return users


def fetch_products_by_category(category: str):
    """Utility function to retrieve products by category using parameterized SQL."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, category, price, stock FROM products WHERE category = ?", (category,))
    products = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return products


if __name__ == "__main__":
    init_database()

