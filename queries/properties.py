from flask import Blueprint, request, jsonify
import sqlite3

properties_bp = Blueprint('properties', __name__)
DB_PATH = 'c:/Projects/energy_app/energy.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@properties_bp.route('/properties', methods=['POST'])
def create_property():
    data = request.json
    conn = get_db()
    cur = conn.cursor()
    print(data)
    cur.execute(
        "INSERT INTO properties (user_id, street_address, city, state_abbreviation, zip) VALUES (?, ?, ?, ?, ?)",
        (data['user_id'], data['street_address'], data['city'], data['state_abbreviation'], data.get('zip'))
    )
    conn.commit()
    property_id = cur.lastrowid
    conn.close()
    return jsonify({'property_id': property_id}), 201

@properties_bp.route('/properties/<int:user_id>', methods=['GET'])
def get_all_properties(user_id):
    conn = get_db()
    properties = conn.execute("SELECT * FROM properties WHERE user_id = ?", (user_id,)).fetchall()
    result = [
        {
            'property_id': row['property_id'],
            'street_address': row['street_address'],
            'city': row['city'],
            'state_abbreviation': row['state_abbreviation'],
            'zip': row['zip']
        }
        for row in properties
    ]
    conn.close()
    return jsonify(result)

@properties_bp.route('/properties/<int:property_id>', methods=['GET'])
def get_property(property_id):
    conn = get_db()
    property = conn.execute("SELECT * FROM properties WHERE property_id = ?", (property_id,)).fetchone()
    if property:
        return dict(property)
    conn.close()
    return {'error': 'Property not found'}, 404

@properties_bp.route('/properties/<int:property_id>', methods=['PUT'])
def update_property(property_id):
    data = request.json
    conn = get_db()
    conn.execute(
        "UPDATE properties SET street_address=?, city=?, state_abbreviation=?, zip_code=? WHERE property_id=?",
        (data['street_address'], data['city'], data['state_abbreviation'], data.get('zip_code'), property_id)
    )
    conn.commit()
    conn.close()
    return {'message': 'Property updated'}

@properties_bp.route('/properties/<int:property_id>', methods=['DELETE'])
def delete_property(property_id):
    conn = get_db()
    conn.execute("DELETE FROM properties WHERE property_id=?", (property_id,))
    conn.commit()
    conn.close()
    return {'message': 'Property deleted'}