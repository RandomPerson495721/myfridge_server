import datetime
import os

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import firebase_admin
from firebase_admin import credentials, auth
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
from models.item import Item
from models.models import db
import uuid





app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///myfridge.db"
# initialize the app with the extension
db.init_app(app)
# Create the database tables
with app.app_context():
    db.create_all()

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

@app.route('/items/get', methods=['GET'])
def get_items():
    # Verify Firebase token
    # decoded_token, error_response = verify_firebase_token()
    # if error_response:
    #     return error_response

    # Get the user ID from the token
    # user_id = decoded_token['uid']
    user_id = "123"  # Placeholder for user ID
    # Query the database for items belonging to the user
    items = Item.query.filter_by(user_id=user_id).all()
    return jsonify([item.to_dict() for item in items])

# Accept an item in JSON format
@app.route('/items/add', methods=['POST'])
def add_item():
    data = request.get_json()

    if not data:
        return jsonify({"message": "No input data provided"}), 400

    # Verify Firebase token
    # decoded_token, error_response = verify_firebase_token()
    # if error_response:
    #     return error_response

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
        user_id="123",  # Placeholder for user ID
       #user_id=decoded_token['uid']  # Assuming user ID is in the token
    )
    db.session.add(item)
    db.session.commit()
    # Return the created item

    return "Item Created", 201


if __name__ == '__main__':
    app.run()
