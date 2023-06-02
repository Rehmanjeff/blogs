from flask import Blueprint, request, jsonify
from pymongo import MongoClient
import datetime
import bcrypt
import main
import jwt
import re



routes = Blueprint('routes', __name__)

@routes.route('/scrape', methods=['POST'])
def scrapeUrl():
    data = request.get_json()
    result = main.scrape(data)
    return result


# Endpoint for the user to register in the mongodb by providing the credentials (name, email, password)
@routes.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    # Check if required fields are provided
    if not name :
        return jsonify({'message': 'Please provide your name'}), 400
    if not email:
        return jsonify({'message':'Please provide your email'}), 400
    if not password:
        return jsonify({'message':'Please provide your password'}), 400
    
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        return jsonify({'message': 'Invalid email address'}), 400

     # Encrypt the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    
    # Connect to the MongoDB database
    client = MongoClient('mongodb://localhost:27017/')
    db = client['blogs']

    # Create the 'users' collection if it doesn't exist
    users_collection = db['users']

    # Create a new user document
    user = {
        'name': name,
        'email': email,
        'password': hashed_password.decode('utf-8'),
    }
    # Insert the user document into the collection
    result = users_collection.insert_one(user)

    
    if result.inserted_id:
        return jsonify({'message': 'User registered successfully'})
    
    else:
        return jsonify({'message': 'Failed to register user'})
    



# Endpoint for the admin to login and get the access token
@routes.route('/admin/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Check if required fields are provided
    if not email:
        return jsonify({'message':'Please provide email'}), 400

    if not password:
        return jsonify({'message': 'Please provide  password'}), 400

    # Connect to the MongoDB database or any other user authentication system
    client = MongoClient('mongodb://localhost:27017/')
    db = client['blogs']
    users_collection = db['users']

    # Find the user document by email
    user = users_collection.find_one({'email': email})

    # Check if the user exists and the password matches
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        
          # Generate access token
        expiration_time = datetime.datetime.utcnow() + datetime.timedelta(days=7)
        payload = {'email': email, 'exp': expiration_time}
        secret_key = 'your_secret_key'  # Replace with your own secret key
        algorithm = 'HS256'
        access_token = jwt.encode(payload, secret_key, algorithm = algorithm)

         # Generate refresh token
        refresh_token_payload = {'email': email}
        refresh_token_secret_key = 'your_refresh_token_secret_key'  # Replace with your own refresh token secret key
        refresh_token_algorithm = 'HS256'
        refresh_token = jwt.encode(refresh_token_payload, refresh_token_secret_key, algorithm=refresh_token_algorithm)
        return jsonify({'message': 'Login successful','user_id': str(user['_id']), 'access_token': access_token, 'refresh_token':refresh_token})
    else:
        return jsonify({'message': 'Invalid credentials'}), 401  
    

    

# Endpoint through which admin provide the valid access token recieve in the login endpoint and get the previliges to access the dashboard 
@routes.route('/admin/dashboard', methods=['GET'])
def admin_dashboard():
    access_token = request.headers.get('Authorization')

    # Check if access token is provided
    if not access_token:
        return jsonify({'message': 'Access token is missing'}), 401

    # Verify and decode the access token
    secret_key = 'your_secret_key'  # Replace with your own secret key
    algorithm = 'HS256'
    try:
        payload = jwt.decode(access_token, secret_key, algorithms=[algorithm])
        email = payload.get('email')

        # Access token is valid, return the user email
        if email:
            return jsonify({'message': 'Access granted', 'email': email})
        else:
            return jsonify({'message': 'Invalid access token'}), 401
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Access token has expired'}), 401
    




@routes.route('/admin/refresh', methods=['POST'])
def refresh_token():
    data = request.get_json()
    refresh_token = data.get('refresh_token')

    # Check if refresh token is provided
    if not refresh_token:
        return jsonify({'message': 'Refresh token is missing'}), 401

    # Verify and decode the refresh token
    refresh_token_secret_key = 'your_refresh_token_secret_key'  # Replace with your own refresh token secret key
    refresh_token_algorithm = 'HS256'
    try:
        payload = jwt.decode(refresh_token, refresh_token_secret_key, algorithms=[refresh_token_algorithm])
        email = payload.get('email')

        # Generate a new access token

        expiration_time = datetime.datetime.utcnow() + datetime.timedelta(days=7)
        access_token_payload = {'email': email, 'exp': expiration_time}
        secret_key = 'your_secret_key'  # Replace with your own secret key
        algorithm = 'HS256'
        access_token = jwt.encode(access_token_payload, secret_key, algorithm=algorithm)

        return jsonify({'message': 'Access token refreshed', 'access_token': access_token})
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Refresh token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid refresh token'}), 401