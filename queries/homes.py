from flask import Blueprint, request, jsonify
import sqlite3

homes_bp = Blueprint('homes', __name__)
DB_PATH = 'c:/Projects/energy_app/energy_app.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@homes_bp.route('/homes', methods=['POST'])
def create_home():
    data = request.json
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO homes (user_id, nickname, zip_code) VALUES (?, ?, ?)",
        (data['user_id'], data['nickname'], data.get('zip_code'))
    )
    conn.commit()
    return jsonify({'home_id': cur.lastrowid}), 201

@homes_bp.route('/homes/<int:home_id>', methods=['GET'])
def get_home(home_id):
    conn = get_db()
    home = conn.execute("SELECT * FROM homes WHERE home_id = ?", (home_id,)).fetchone()
    if home:
        return dict(home)
    return {'error': 'Home not found'}, 404

@homes_bp.route('/homes/<int:home_id>', methods=['PUT'])
def update_home(home_id):
    data = request.json
    conn = get_db()
    conn.execute(
        "UPDATE homes SET nickname=?, zip_code=? WHERE home_id=?",
        (data['nickname'], data.get('zip_code'), home_id)
    )
    conn.commit()
    return {'message': 'Home updated'}

@homes_bp.route('/homes/<int:home_id>', methods=['DELETE'])
def delete_home(home_id):
    conn = get_db()
    conn.execute("DELETE FROM homes WHERE home_id=?", (home_id,))
    conn.commit()
    return {'message': 'Home deleted'}