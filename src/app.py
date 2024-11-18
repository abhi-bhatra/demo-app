# src/app.py
from flask import Flask, request, jsonify
import sqlite3
import yaml
import json
import pickle
import os
from werkzeug.security import generate_password_hash

app = Flask(__name__)

SECRET_KEY = "hardcoded_super_secret_key"
DATABASE_PASSWORD = "hardcoded_db_password"

# Using the secret key in an unsafe way
@app.route('/get_secret')
def get_secret():
    # Return the secret key directly, simulating an insecure use of secrets
    return jsonify({"secret_key": SECRET_KEY})

# Vulnerability 2: Insecure database connection
def get_db_connection():
    # Using the exposed database password in the connection (simulated usage)
    conn = sqlite3.connect(f"file:database.db?password={DATABASE_PASSWORD}", uri=True)
    return conn

# Vulnerability 3: SQL Injection vulnerability
@app.route('/users/<username>')
def get_user(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Unsafe SQL query
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    conn.close()
    return jsonify({"user": user})

# Vulnerability 4: Insecure deserialization
@app.route('/load_data', methods=['POST'])
def load_data():
    data = request.get_data()
    # Safe JSON deserialization
    return json.loads(data)

# Vulnerability 5: Path traversal vulnerability
@app.route('/get_file/<path>')
def get_file(path):
    # Unsafe file access
    with open(path, 'r') as file:
        content = file.read()
    return content

# Vulnerability 6: Unsafe YAML parsing
@app.route('/parse_config', methods=['POST'])
def parse_config():
    config_data = request.get_data().decode('utf-8')
    # Safe YAML parsing
    return yaml.safe_load(config_data)

# Vulnerability 7: Weak password hashing
@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Using an outdated hashing method
    hashed_password = generate_password_hash(password, method='sha256')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, hashed_password)
    )
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)  # Vulnerability 8: Debug mode enabled in production
