import datetime
import os

from flask import Flask, jsonify, request
import firebase_admin
from firebase_admin import credentials, auth
from datetime import datetime
from models.item import Item
from models.models import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///myfridge.db"
db.init_app(app)
with app.app_context():
    db.create_all()

key_path = os.environ.get("FIREBASE_ADMIN_SDK_KEY_PATH")
cred = credentials.Certificate(key_path)
firebase_admin.initialize_app(cred)

def verify_firebase_token():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None, jsonify({"message": "Missing or invalid token"}), 401

    id_token = auth_header.split(" ")[1]
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token, None
    except Exception as e:
        return None, jsonify({"message": "Invalid token", "error": str(e)}), 401

@app.route('/items/get', methods=['GET'])
def get_items():
    decoded_token, error_response = verify_firebase_token()
    if error_response:
        return error_response

    user_id: str = decoded_token['uid']
    items = Item.query.filter_by(user_id=user_id).all()
    return jsonify([item.to_dict() for item in items])

@app.route('/items/add', methods=['POST'])
def add_item():
    data = request.get_json()

    if not data:
        return jsonify({"message": "No input data provided"}), 400

    decoded_token, error_response = verify_firebase_token()
    if error_response:
        return error_response

    expiration: datetime = datetime(1970, 1, 1)
    try:
        expiration = datetime.strptime(data.get('expiration_date'), '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        return jsonify({"message": "Invalid date format"}), 400

    # Create a new item
    item = Item(
        name=data.get('name'),
        description=data.get('description'),
        quantity=data.get('quantity'),
        expiration_date=expiration,
        position=data.get('position'),
        user_id=decoded_token['uid'],
        image_url=data.get('image_url')
    )
    db.session.add(item)
    db.session.commit()

    return "Item Created", 201

@app.route('/items/update/<string:reference_id>', methods=['PUT'])
def update_item(reference_id):
    data = request.get_json()

    if not data:
        return jsonify({"message": "No input data provided"}), 400

    decoded_token, error_response = verify_firebase_token()
    if error_response:
        return error_response

    item = Item.query.filter_by(reference_id=reference_id).first()
    if not item:
        return jsonify({"message": "Item not found"}), 404

    if item.user_id != decoded_token['uid']:
        return jsonify({"message": "Unauthorized"}), 403

    item.name = data.get('name', item.name)
    item.description = data.get('description', item.description)
    item.quantity = data.get('quantity', item.quantity)
    try:
        item.expiration_date = datetime.strptime(data.get('expiration_date'), '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        return jsonify({"message": "Invalid date format"}), 400
    item.position = data.get('position', item.position)
    item.image_url = data.get('image_url', item.image_url)



    db.session.add(item)
    db.session.commit()

    return jsonify(item.to_dict()), 200

@app.route('/items/delete/<string:reference_id>', methods=['DELETE'])
def delete_item(reference_id):
    # Verify Firebase token
    decoded_token, error_response = verify_firebase_token()
    if error_response:
        return error_response

    item = Item.query.filter_by(reference_id=reference_id).first()
    if not item:
        return jsonify({"message": "Item not found"}), 404

    if item.user_id != decoded_token['uid']:
        return jsonify({"message": "Unauthorized"}), 403

    db.session.delete(item)
    db.session.commit()

    return "Item Deleted", 200


if __name__ == '__main__':
    app.run()
