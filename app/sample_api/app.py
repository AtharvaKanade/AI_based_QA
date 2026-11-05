"""
Sample E-Commerce REST API - System Under Test (SUT)
Provides endpoints for Authentication, Users, and Products.
"""

from flask import Flask, jsonify, request
import sqlite3
import os
import uuid

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "test_data.db")

VALID_TOKENS = {
    "admin-token-xyz": {"role": "admin", "username": "admin_user"},
    "standard-token-abc": {"role": "customer", "username": "standard_user"}
}


def get_db_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "ecommerce-api", "version": "1.0.0"}), 200


@app.route("/api/v1/auth/login", methods=["POST"])
def login():
    """Authenticate user and return JWT/bearer token"""
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role, status FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        if user["status"] == "locked":
            return jsonify({"error": "Account is locked"}), 403
        
        token = "admin-token-xyz" if user["role"] == "admin" else "standard-token-abc"
        return jsonify({
            "message": "Login successful",
            "token": token,
            "user": {
                "id": user["id"],
                "username": user["username"],
                "role": user["role"]
            }
        }), 200
    
    return jsonify({"error": "Invalid username or password"}), 401


@app.route("/api/v1/products", methods=["GET"])
def get_products():
    """Retrieve list of products with optional category and max_price filters"""
    category = request.args.get("category")
    max_price = request.args.get("max_price", type=float)

    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT id, name, category, price, stock FROM products WHERE 1=1"
    params = []

    if category:
        query += " AND category = ?"
        params.append(category)
    if max_price is not None:
        query += " AND price <= ?"
        params.append(max_price)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    products = [dict(row) for row in rows]
    return jsonify({"count": len(products), "products": products}), 200


@app.route("/api/v1/products/<int:product_id>", methods=["GET"])
def get_product_by_id(product_id):
    """Retrieve single product by ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, category, price, stock FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    conn.close()

    if product is None:
        return jsonify({"error": f"Product with ID {product_id} not found"}), 404

    return jsonify(dict(product)), 200


@app.route("/api/v1/products", methods=["POST"])
def create_product():
    """Create a new product (Admin authorization required)"""
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "").strip()

    if token not in VALID_TOKENS or VALID_TOKENS[token]["role"] != "admin":
        return jsonify({"error": "Unauthorized: Admin privileges required"}), 403

    data = request.get_json() or {}
    name = data.get("name")
    category = data.get("category")
    price = data.get("price")
    stock = data.get("stock", 0)

    if not name or price is None or price < 0:
        return jsonify({"error": "Invalid product payload. Name and non-negative price required."}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, category, price, stock) VALUES (?, ?, ?, ?)",
                   (name, category, price, stock))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return jsonify({"message": "Product created successfully", "product_id": new_id}), 201


@app.route("/api/v1/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    """Delete a product by ID (Admin authorization required)"""
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "").strip()

    if token not in VALID_TOKENS or VALID_TOKENS[token]["role"] != "admin":
        return jsonify({"error": "Unauthorized: Admin privileges required"}), 403

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM products WHERE id = ?", (product_id,))
    if cursor.fetchone() is None:
        conn.close()
        return jsonify({"error": f"Product with ID {product_id} not found"}), 404

    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": f"Product {product_id} deleted successfully"}), 200


if __name__ == "__main__":
    app.run(port=5000, debug=True)

