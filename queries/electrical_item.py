from flask import Blueprint, request, jsonify
import sqlite3

electrical_item_bp = Blueprint('electrical_item', __name__)
DB_PATH = 'c:/Projects/energy_app/energy_app.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@electrical_item_bp.route('/electrical_items', methods=['POST'])
def create_electrical_item():
    data = request.json
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO electrical_item (home_id, category_id, usage_type_id, nickname, rated_watts) VALUES (?, ?, ?, ?, ?)",
        (data['home_id'], data['category_id'], data['usage_type_id'], data['nickname'], data.get('rated_watts'))
    )
    conn.commit()
    return jsonify({'item_id': cur.lastrowid}), 201

@electrical_item_bp.route('/electrical_items/<int:item_id>', methods=['GET'])
def get_electrical_item(item_id):
    conn = get_db()
    item = conn.execute("SELECT * FROM electrical_item WHERE item_id = ?", (item_id,)).fetchone()
    if item:
        return dict(item)
    return {'error': 'Electrical item not found'}, 404

@electrical_item_bp.route('/electrical_items/home/<int:home_id>', methods=['GET'])
def get_electrical_items_by_home(home_id):
    conn = get_db()
    items = conn.execute("SELECT * FROM electrical_item WHERE home_id = ?", (home_id,)).fetchall()
    return jsonify([dict(row) for row in items])

@electrical_item_bp.route('/electrical_items/<int:item_id>', methods=['PUT'])
def update_electrical_item(item_id):
    data = request.json
    conn = get_db()
    updates = []
    params = []
    if 'nickname' in data:
        updates.append("nickname = ?")
        params.append(data['nickname'])
    if 'rated_watts' in data:
        updates.append("rated_watts = ?")
        params.append(data['rated_watts'])
    if 'category_id' in data:
        updates.append("category_id = ?")
        params.append(data['category_id'])
    if 'usage_type_id' in data:
        updates.append("usage_type_id = ?")
        params.append(data['usage_type_id'])
    if not updates:
        return {'message': 'No fields to update'}, 400
    params.append(item_id)
    sql = f"UPDATE electrical_item SET {', '.join(updates)} WHERE item_id = ?"
    conn.execute(sql, params)
    conn.commit()
    return {'message': 'Electrical item updated'}

@electrical_item_bp.route('/electrical_items/<int:item_id>', methods=['DELETE'])
def delete_electrical_item(item_id):
    conn = get_db()
    conn.execute("DELETE FROM electrical_item WHERE item_id = ?", (item_id,))
    conn.commit()
    return {'message': 'Electrical item deleted'}