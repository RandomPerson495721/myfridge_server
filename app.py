import os

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import firebase_admin
from firebase_admin import credentials, auth
from sqlalchemy.orm import DeclarativeBase

from models.item import Item
from models.models import db

app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///myfridge.db"
# initialize the app with the extension
db.init_app(app)

# Initialize Firebase Admin SDK
key_path = os.environ.get("FIREBASE_ADMIN_SDK_KEY_PATH")
cred = credentials.Certificate(key_path)  # Replace with your Firebase service account key
firebase_admin.initialize_app(cred)

# Function to verify Firebase ID token
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

@app.route('/')
def hello_world():  # put application's code here
    a = Item('item1', 'description1', 10, 1234567890)
    json_data = jsonify(a.to_dict())
    return json_data

@app.route('/items', methods=['GET'])
def get_items():
    # Verify Firebase token
    decoded_token, error_response = verify_firebase_token()
    if error_response:
        return error_response
    items = [
        Item('item1', 'description1', 10, 1234567890),
        Item('item2', 'description2', 20, 1234567890)
    ]
    return jsonify([item.to_dict() for item in items])

# Accept an item in JSON format
@app.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()

    if not data:
        return jsonify({"message": "No input data provided"}), 400

    # Verify Firebase token
    decoded_token, error_response = verify_firebase_token()
    if error_response:
        return error_response

    # Create a new item
    item = Item(
        name=data.get('name'),
        description=data.get('description'),
        quantity=data.get('quantity'),
        expiration_date=data.get('expiration_date'),
        position=data.get('position'),
        user_id=decoded_token['uid']  # Assuming user ID is in the token
    )
    db.session.add(item)
    db.session.commit()
    # Return the created item

    return jsonify(item.to_dict()), 201


if __name__ == '__main__':
    app.run()
