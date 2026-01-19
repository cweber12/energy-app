from flask import Blueprint, request, jsonify
import sqlite3

meter_hourly_reading_bp = Blueprint('meter_hourly_reading', __name__)
DB_PATH = 'c:/Projects/energy_app/energy_app.db'

def get_db():
	conn = sqlite3.connect(DB_PATH)
	conn.row_factory = sqlite3.Row
	return conn

@meter_hourly_reading_bp.route('/meter_hourly_readings', methods=['POST'])
def create_meter_hourly_reading():
	data = request.json
	conn = get_db()
	cur = conn.cursor()
	cur.execute(
		"INSERT INTO meter_hourly_reading (meter_id, start_ts, end_ts, consumed_kwh) VALUES (?, ?, ?, ?)",
		(data['meter_id'], data['start_ts'], data['end_ts'], data['consumed_kwh'])
	)
	conn.commit()
	return jsonify({'reading_id': cur.lastrowid}), 201

@meter_hourly_reading_bp.route('/meter_hourly_readings/<int:reading_id>', methods=['GET'])
def get_meter_hourly_reading(reading_id):
	conn = get_db()
	reading = conn.execute("SELECT * FROM meter_hourly_reading WHERE reading_id = ?", (reading_id,)).fetchone()
	if reading:
		return dict(reading)
	return {'error': 'Meter hourly reading not found'}, 404

@meter_hourly_reading_bp.route('/meter_hourly_readings/meter/<int:meter_id>', methods=['GET'])
def get_meter_hourly_readings_by_meter(meter_id):
	conn = get_db()
	readings = conn.execute("SELECT * FROM meter_hourly_reading WHERE meter_id = ?", (meter_id,)).fetchall()
	return jsonify([dict(row) for row in readings])

@meter_hourly_reading_bp.route('/meter_hourly_readings/<int:reading_id>', methods=['PUT'])
def update_meter_hourly_reading(reading_id):
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
	if 'consumed_kwh' in data:
		updates.append("consumed_kwh = ?")
		params.append(data['consumed_kwh'])
	if 'meter_id' in data:
		updates.append("meter_id = ?")
		params.append(data['meter_id'])
	if not updates:
		return {'message': 'No fields to update'}, 400
	params.append(reading_id)
	sql = f"UPDATE meter_hourly_reading SET {', '.join(updates)} WHERE reading_id = ?"
	conn.execute(sql, params)
	conn.commit()
	return {'message': 'Meter hourly reading updated'}

@meter_hourly_reading_bp.route('/meter_hourly_readings/<int:reading_id>', methods=['DELETE'])
def delete_meter_hourly_reading(reading_id):
	conn = get_db()
	conn.execute("DELETE FROM meter_hourly_reading WHERE reading_id = ?", (reading_id,))
	conn.commit()
	return {'message': 'Meter hourly reading deleted'}
