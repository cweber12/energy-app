from flask import Blueprint, request, jsonify
import sqlite3
from utils.encrypt_password import encrypt_password, check_password

users_bp = Blueprint('users', __name__)
DB_PATH = 'c:/Projects/energy_app/energy.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@users_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    conn = get_db()
    cur = conn.cursor()
    user = cur.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    if user and check_password(password, user['password_hash']):
        conn.close()
        return jsonify({'user_id': user['user_id'], 'username': user['username'], 'email': user['email']})
    conn.close()
    return {'error': 'Invalid email or password'}, 401

@users_bp.route('/users', methods=['POST'])
def create_user():
    data = request.json
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * from users WHERE username = ?", (data['username'],))
    if cur.fetchone() is not None:
        conn.close()
        return {'error': 'Username already exists'}, 400
    cur.execute(
        "INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)",
        (data['username'], encrypt_password(data['password']), data['email'])
    )
    conn.commit()
    conn.close()
    return jsonify({'user_id': cur.lastrowid}), 201

@users_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_db()
    cur = conn.cursor()
    user = cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
    if user:
        conn.close()
        return dict(user)
    conn.close()
    return {'error': 'User not found'}, 404

@users_bp.route('/users/<int:user_id>/<string:email>', methods=['GET'])
def get_user_by_credentials(email, password):
    password_hash = encrypt_password(password)
    conn = get_db()
    cur = conn.cursor()
    user = cur.execute(
        "SELECT * FROM users WHERE email = ? AND password_hash = ?",
        (email, password_hash)
    ).fetchone()
    if user:
        conn.close()
        return dict(user)
    conn.close()
    return {'error': 'User not found or invalid credentials'}, 404

@users_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "UPDATE users SET username=?, password_hash=?, email=? WHERE user_id=?",
        (data['username'], data['password_hash'], data['email'], user_id)
    )
    conn.commit()
    conn.close()
    return {'message': 'User updated'}

@users_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()
    return {'message': 'User deleted'}