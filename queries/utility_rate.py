from flask import Blueprint, request, jsonify
import sqlite3

utility_rate_bp = Blueprint('utility_rate', __name__)
DB_PATH = 'c:/Projects/energy_app/energy_app.db'

def get_db():
	conn = sqlite3.connect(DB_PATH)
	conn.row_factory = sqlite3.Row
	return conn

@utility_rate_bp.route('/utility_rates', methods=['POST'])
def create_utility_rate():
	data = request.json
	conn = get_db()
	cur = conn.cursor()
	cur.execute(
		"INSERT INTO monthly_utility_rate (home_id, month_year, bill, consumed_kwh) VALUES (?, ?, ?, ?)",
		(data['home_id'], data['month_year'], data['bill'], data['consumed_kwh'])
	)
	conn.commit()
	return jsonify({'rate_id': cur.lastrowid}), 201

@utility_rate_bp.route('/utility_rates/<int:rate_id>', methods=['GET'])
def get_utility_rate(rate_id):
	conn = get_db()
	rate = conn.execute("SELECT * FROM monthly_utility_rate WHERE rate_id = ?", (rate_id,)).fetchone()
	if rate:
		return dict(rate)
	return {'error': 'Utility rate not found'}, 404

@utility_rate_bp.route('/utility_rates/home/<int:home_id>', methods=['GET'])
def get_utility_rates_by_home(home_id):
	conn = get_db()
	rates = conn.execute("SELECT * FROM monthly_utility_rate WHERE home_id = ?", (home_id,)).fetchall()
	return jsonify([dict(row) for row in rates])

@utility_rate_bp.route('/utility_rates/<int:rate_id>', methods=['PUT'])
def update_utility_rate(rate_id):
	data = request.json
	conn = get_db()
	updates = []
	params = []
	if 'month_year' in data:
		updates.append("month_year = ?")
		params.append(data['month_year'])
	if 'bill' in data:
		updates.append("bill = ?")
		params.append(data['bill'])
	if 'consumed_kwh' in data:
		updates.append("consumed_kwh = ?")
		params.append(data['consumed_kwh'])
	if 'home_id' in data:
		updates.append("home_id = ?")
		params.append(data['home_id'])
	if not updates:
		return {'message': 'No fields to update'}, 400
	params.append(rate_id)
	sql = f"UPDATE monthly_utility_rate SET {', '.join(updates)} WHERE rate_id = ?"
	conn.execute(sql, params)
	conn.commit()
	return {'message': 'Utility rate updated'}

@utility_rate_bp.route('/utility_rates/<int:rate_id>', methods=['DELETE'])
def delete_utility_rate(rate_id):
	conn = get_db()
	conn.execute("DELETE FROM monthly_utility_rate WHERE rate_id = ?", (rate_id,))
	conn.commit()
	return {'message': 'Utility rate deleted'}
