from flask import Blueprint, request, jsonify
from models.user_model import UserModel
from config.config import db
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)
user_model = UserModel(db)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Username, email and password are required"}), 400

    if user_model.get_email(data['email']):
        return jsonify({"error": "User already exists"}), 409

    password_hash = generate_password_hash(data['password'])
    user_model.create_user(data['username'], data['email'], password_hash)
    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = user_model.get_email(data.get('email'))

    if not user or not check_password_hash(user['password_hash'], data['password']):
        return jsonify({"error": "Invalid email or password"}), 401

    return jsonify({"message": "Login successful", "user": user['email']}), 200
