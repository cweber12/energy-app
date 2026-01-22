from flask import Blueprint, request, jsonify
import sqlite3

item_usage_event_bp = Blueprint('item_usage_event', __name__)
DB_PATH = 'c:/Projects/energy_app/energy.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Create a new start event
@item_usage_event_bp.route('/item_usage_event_start', methods=['POST'])
def create_item_usage_event_start():
    data = request.json
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO item_usage_event_start (item_id, start_ts) VALUES (?, ?)",
        (data['item_id'], data['start_ts'])
    )
    conn.commit()
    event_id = cur.lastrowid
    conn.close()
    return jsonify({'event_id': event_id, 'start_ts': data['start_ts']}), 201

# Create a new end event (must reference an existing start event)
@item_usage_event_bp.route('/item_usage_event_end', methods=['POST'])
def create_item_usage_event_end():
    data = request.json
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO item_usage_event_end (event_id, end_ts) VALUES (?, ?)",
        (data['event_id'], data['end_ts'])
    )
    conn.commit()
    conn.close()
    return jsonify({'event_id': data['event_id'], 'end_ts': data['end_ts']}), 201

# Get the most recent start_ts for an item
@item_usage_event_bp.route('/item_usage_event_start/item/<int:item_id>/latest_start', methods=['GET'])
def get_latest_start_ts_by_item(item_id):
    conn = get_db()
    event = conn.execute(
        "SELECT event_id, start_ts FROM item_usage_event_start WHERE item_id = ? ORDER BY start_ts DESC LIMIT 1",
        (item_id,)
    ).fetchone()
    conn.close()
    if event:
        return jsonify({'event_id': event['event_id'], 'latest_start_ts': event['start_ts']})
    return jsonify({'error': 'No start events found for this item'}), 404

# Get the most recent end_ts for an item (by joining to latest start event)
@item_usage_event_bp.route('/item_usage_event_end/item/<int:item_id>/latest_end', methods=['GET'])
def get_latest_end_ts_by_item(item_id):
    conn = get_db()
    event = conn.execute(
        """
        SELECT e.event_id, e.end_ts
        FROM item_usage_event_start s
        JOIN item_usage_event_end e ON s.event_id = e.event_id
        WHERE s.item_id = ?
        ORDER BY s.start_ts DESC LIMIT 1
        """,
        (item_id,)
    ).fetchone()
    conn.close()
    if event:
        return jsonify({'event_id': event['event_id'], 'latest_end_ts': event['end_ts']})
    return jsonify({'error': 'No end events found for this item'}), 404

# Update a start event
@item_usage_event_bp.route('/item_usage_event_start/', methods=['PUT'])
def update_item_usage_event_start():
    data = request.json
    if 'start_ts' not in data:
        return {'message': 'No start_ts provided'}, 400
    conn = get_db()
    conn.execute(
        "UPDATE item_usage_event_start SET start_ts = ?",
        (data['start_ts'])
    )
    conn.commit()
    conn.close()
    return {'message': 'Start event updated'}

# Update an end event
@item_usage_event_bp.route('/item_usage_event_end/<int:event_id>', methods=['PUT'])
def update_item_usage_event_end(event_id):
    data = request.json
    if 'end_ts' not in data:
        return {'message': 'No end_ts provided'}, 400
    conn = get_db()
    conn.execute(
        "UPDATE item_usage_event_end SET end_ts = ? WHERE event_id = ?",
        (data['end_ts'], event_id)
    )
    conn.commit()
    conn.close()
    return {'message': 'End event updated'}