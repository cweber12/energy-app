from flask import Blueprint, request, jsonify
import sqlite3
from utils.encrypt_password import encrypt_password, check_password

users_bp = Blueprint('users', __name__)
DB_PATH = 'c:/Projects/energy_app/energy_app.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@users_bp.route('/users', methods=['POST'])
def create_user():
    data = request.json
    conn = get_db()
    conn.execute("SELECT * from users WHERE username = ?", (data['username'],))
    if conn.fetchone() is not None:
        return {'error': 'Username already exists'}, 400
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)",
        (data['username'], encrypt_password(data['password']), data['email'])
    )
    conn.commit()
    return jsonify({'user_id': cur.lastrowid}), 201

@users_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
    if user:
        return dict(user)
    return {'error': 'User not found'}, 404

@users_bp.route('/users/<int:user_id>/<string:password_hash>', methods=['GET'])
def get_user_by_credentials(user_id, password_hash):
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE user_id = ? AND password_hash = ?",
        (user_id, password_hash)
    ).fetchone()
    if user:
        return dict(user)
    return {'error': 'User not found or invalid credentials'}, 404

@users_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    conn = get_db()
    conn.execute(
        "UPDATE users SET username=?, password_hash=?, email=? WHERE user_id=?",
        (data['username'], data['password_hash'], data['email'], user_id)
    )
    conn.commit()
    return {'message': 'User updated'}

@users_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_db()
    conn.execute("DELETE FROM users WHERE user_id=?", (user_id,))
    conn.commit()
    return {'message': 'User deleted'}