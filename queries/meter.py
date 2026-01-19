from flask import Blueprint, request, jsonify
import sqlite3

meter_bp = Blueprint('meter', __name__)
DB_PATH = 'c:/Projects/energy_app/energy_app.db'

def get_db():
	conn = sqlite3.connect(DB_PATH)
	conn.row_factory = sqlite3.Row
	return conn

@meter_bp.route('/meters', methods=['POST'])
def create_meter():
	data = request.json
	conn = get_db()
	cur = conn.cursor()
	cur.execute(
		"INSERT INTO meter (home_id, utility_meter_number) VALUES (?, ?)",
		(data['home_id'], data['utility_meter_number'])
	)
	conn.commit()
	return jsonify({'meter_id': cur.lastrowid}), 201

@meter_bp.route('/meters/<int:meter_id>', methods=['GET'])
def get_meter(meter_id):
	conn = get_db()
	meter = conn.execute("SELECT * FROM meter WHERE meter_id = ?", (meter_id,)).fetchone()
	if meter:
		return dict(meter)
	return {'error': 'Meter not found'}, 404

@meter_bp.route('/meters', methods=['GET'])
def get_all_meters():
	conn = get_db()
	meters = conn.execute("SELECT * FROM meter").fetchall()
	return jsonify([dict(row) for row in meters])

@meter_bp.route('/meters/<int:meter_id>', methods=['PUT'])
def update_meter(meter_id):
	data = request.json
	conn = get_db()
	conn.execute(
		"UPDATE meter SET home_id=?, utility_meter_number=? WHERE meter_id=?",
		(data['home_id'], data['utility_meter_number'], meter_id)
	)
	conn.commit()
	return {'message': 'Meter updated'}

@meter_bp.route('/meters/<int:meter_id>', methods=['DELETE'])
def delete_meter(meter_id):
	conn = get_db()
	conn.execute("DELETE FROM meter WHERE meter_id=?", (meter_id,))
	conn.commit()
	return {'message': 'Meter deleted'}
