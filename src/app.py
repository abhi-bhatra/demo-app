# src/app.py
from flask import Flask, request, jsonify
import sqlite3
import yaml
import pickle
import os
from werkzeug.security import generate_password_hash

app = Flask(__name__)

# Vulnerability 1: Hardcoded credentials
DB_PASSWORD = "super_secret_password123"
API_KEY = "1234567890abcdef"

# Vulnerability 2: Insecure database connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    return conn

# Vulnerability 3: SQL Injection vulnerability
@app.route('/users/<username>')
def get_user(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Unsafe SQL query
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()
    return jsonify({"user": user})

# Vulnerability 4: Insecure deserialization
@app.route('/load_data', methods=['POST'])
def load_data():
    data = request.get_data()
    # Unsafe pickle deserialization
    return pickle.loads(data)

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
    # Unsafe YAML parsing
    return yaml.load(config_data, Loader=yaml.Loader)

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
