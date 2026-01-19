from flask import Blueprint, request, jsonify
import sqlite3

item_category_bp = Blueprint('item_category', __name__)
DB_PATH = 'c:/Projects/energy_app/energy_app.db'

def get_db():
	conn = sqlite3.connect(DB_PATH)
	conn.row_factory = sqlite3.Row
	return conn

@item_category_bp.route('/item_categories', methods=['POST'])
def create_item_category():
	data = request.json
	conn = get_db()
	cur = conn.cursor()
	cur.execute(
		"INSERT INTO item_category (category_name) VALUES (?)",
		(data['category_name'],)
	)
	conn.commit()
	return jsonify({'category_id': cur.lastrowid}), 201

@item_category_bp.route('/item_categories/<int:category_id>', methods=['GET'])
def get_item_category(category_id):
	conn = get_db()
	category = conn.execute("SELECT * FROM item_category WHERE category_id = ?", (category_id,)).fetchone()
	if category:
		return dict(category)
	return {'error': 'Item category not found'}, 404

@item_category_bp.route('/item_categories', methods=['GET'])
def get_all_item_categories():
	conn = get_db()
	categories = conn.execute("SELECT * FROM item_category").fetchall()
	return jsonify([dict(row) for row in categories])

@item_category_bp.route('/item_categories/<int:category_id>', methods=['PUT'])
def update_item_category(category_id):
	data = request.json
	conn = get_db()
	conn.execute(
		"UPDATE item_category SET category_name=? WHERE category_id=?",
		(data['category_name'], category_id)
	)
	conn.commit()
	return {'message': 'Item category updated'}

@item_category_bp.route('/item_categories/<int:category_id>', methods=['DELETE'])
def delete_item_category(category_id):
	conn = get_db()
	conn.execute("DELETE FROM item_category WHERE category_id=?", (category_id,))
	conn.commit()
	return {'message': 'Item category deleted'}
