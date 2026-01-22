from flask import Blueprint, request, jsonify
import sqlite3

usage_type_bp = Blueprint('usage_type', __name__)
DB_PATH = 'c:/Projects/energy_app/energy.db'

def get_db():
	conn = sqlite3.connect(DB_PATH)
	conn.row_factory = sqlite3.Row
	return conn

@usage_type_bp.route('/usage_types', methods=['POST'])
def create_usage_type():
	data = request.json
	conn = get_db()
	cur = conn.cursor()
	cur.execute(
		"INSERT INTO usage_type (usage_type_name) VALUES (?)",
		(data['usage_type_name'],)
	)
	conn.commit()
	conn.close()
	return jsonify({'usage_type_id': cur.lastrowid}), 201

@usage_type_bp.route('/usage_types/<int:usage_type_id>', methods=['GET'])
def get_usage_type(usage_type_id):
	conn = get_db()
	usage = conn.execute("SELECT * FROM usage_type WHERE usage_type_id = ?", (usage_type_id,)).fetchone()
	if usage:
		conn.close()
		return dict(usage)
	conn.close()
	return {'error': 'Usage type not found'}, 404

@usage_type_bp.route('/usage_types', methods=['GET'])
def get_all_usage_types():
	conn = get_db()
	usages = conn.execute("SELECT * FROM usage_type").fetchall()
	conn.close()
	return jsonify([dict(row) for row in usages])

@usage_type_bp.route('/usage_types/<int:usage_type_id>', methods=['PUT'])
def update_usage_type(usage_type_id):
	data = request.json
	conn = get_db()
	conn.execute(
		"UPDATE usage_type SET usage_type_name=? WHERE usage_type_id=?",
		(data['usage_type_name'], usage_type_id)
	)
	conn.commit()
	conn.close()
	return {'message': 'Usage type updated'}

@usage_type_bp.route('/usage_types/<int:usage_type_id>', methods=['DELETE'])
def delete_usage_type(usage_type_id):
	conn = get_db()
	conn.execute("DELETE FROM usage_type WHERE usage_type_id=?", (usage_type_id,))
	conn.commit()
	conn.close()
	return {'message': 'Usage type deleted'}
