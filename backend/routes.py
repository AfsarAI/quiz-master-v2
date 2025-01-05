from flask import current_app as app, Blueprint, jsonify, render_template, request, send_from_directory
from flask_security import auth_required, verify_password, hash_password
from models import db

datastore = app.security.datastore

@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400
    
    user = datastore.find_user(email=email)
    if user:
        return jsonify({'message': 'User already exists'}), 400
    
    try:
        user = datastore.create_user(email=email, password=hash_password(password), roles=[role])
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500
    return jsonify({'message': 'User created successfully'}), 201



@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400
    
    user = datastore.find_user(email=email)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    if verify_password(password, user.password):
        return jsonify({'token': user.get_auth_token(), 'email': user.email, 'message': 'Logged in successfully'}), 200
    
    return jsonify({'message': 'Invalid password'}), 401