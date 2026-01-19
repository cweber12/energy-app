from flask import Blueprint, request, jsonify
import sqlite3

item_usage_event_bp = Blueprint('item_usage_event', __name__)
DB_PATH = 'c:/Projects/energy_app/energy_app.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@item_usage_event_bp.route('/item_usage_events', methods=['POST'])
def create_item_usage_event():
    data = request.json
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO item_usage_event (item_id, start_ts, end_ts) VALUES (?, ?, ?)",
        (data['item_id'], data['start_ts'], data.get('end_ts'))
    )
    conn.commit()
    return jsonify({'event_id': cur.lastrowid}), 201

@item_usage_event_bp.route('/item_usage_events/<int:event_id>', methods=['GET'])
def get_item_usage_event(event_id):
    conn = get_db()
    event = conn.execute("SELECT * FROM item_usage_event WHERE event_id = ?", (event_id,)).fetchone()
    if event:
        return dict(event)
    return {'error': 'Item usage event not found'}, 404

@item_usage_event_bp.route('/item_usage_events/item/<int:item_id>', methods=['GET'])
def get_item_usage_events_by_item(item_id):
    conn = get_db()
    events = conn.execute("SELECT * FROM item_usage_event WHERE item_id = ?", (item_id,)).fetchall()
    return jsonify([dict(row) for row in events])

@item_usage_event_bp.route('/item_usage_events/<int:event_id>', methods=['PUT'])
def update_item_usage_event(event_id):
    data = request.json
    conn = get_db()
    updates = []
    params = []
    if 'start_ts' in data:
        updates.append("start_ts = ?")
        params.append(data['start_ts'])
    if 'end_ts' in data:
        updates.append("end_ts = ?")
        params.append(data['end_ts'])
    if not updates:
        return {'message': 'No fields to update'}, 400
    params.append(event_id)
    sql = f"UPDATE item_usage_event SET {', '.join(updates)} WHERE event_id = ?"
    conn.execute(sql, params)
    conn.commit()
    return {'message': 'Item usage event updated'}

@item_usage_event_bp.route('/item_usage_events/<int:event_id>', methods=['DELETE'])
def delete_item_usage_event(event_id):
    conn = get_db()
    conn.execute("DELETE FROM item_usage_event WHERE event_id = ?", (event_id,))
    conn.commit()
    return {'message': 'Item usage event deleted'}