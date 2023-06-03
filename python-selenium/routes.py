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

        users_collection.update_one({'_id': user['_id']}, {'$set': {'access_token': access_token}})
        users_collection.update_one({'_id': user['_id']}, {'$set': {'refresh_token': refresh_token}})

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

        # Connect to the MongoDB database or any other user authentication system
        client = MongoClient('mongodb://localhost:27017/')
        db = client['blogs']
        users_collection = db['users']

        # Find the user document by email and access token
        user = users_collection.find_one({'email': email, 'access_token': access_token})

        if user:
            # Access token is valid and present in the database, return the user email
            return jsonify({'message': 'Access granted', 'email': email})
        else:
            return jsonify({'message': "Token dosen't exists in database"}), 401
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Access token has expired'}), 401 
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid refresh token'}), 401   
    




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
    


@routes.route('/admin/logout', methods=['POST'])
def logout():
    auth_header = request.headers.get('Authorization')

    if auth_header and auth_header.startswith('Bearer '):
        access_token = auth_header.split(' ')[1]

        # Decode the access token
        try:
            secret_key = 'your_secret_key'  # Replace with your own secret key
            payload = jwt.decode(access_token, secret_key, algorithms=['HS256'])
            email = payload['email']

            # Retrieve the user based on the email
            client = MongoClient('mongodb://localhost:27017/')
            db = client['blogs']
            users_collection = db['users']
            user = users_collection.find_one({'email': email})

            if user:
                # Clear the access token
                user['access_token'] = None
                user['refresh_token'] = None

                # Update the user document in the database
                users_collection.update_one({'_id': user['_id']}, {'$set': user})

                return jsonify({'message': 'Logout successful'})

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Access token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid access token'}), 401

    return jsonify({'message': 'Invalid authorization header'}), 401



@routes.route('/admin/category', methods=['POST'])
def create_category():
    auth_header = request.headers.get('Authorization')
    data = request.get_json()

    # Extract the necessary data from the request
    name = data.get('name')

    # Connect to the MongoDB database
    client = MongoClient('mongodb://localhost:27017/')
    db = client['blogs']

    # Create the 'category' collection if it doesn't exist
    categories_collection = db['category']

    if not auth_header:
        return jsonify({'message': 'Token is missing'}), 400

    # Extract the token from the "Bearer <token>" format
    token = auth_header.split(' ')[1]

    try:
        # Verify and decode the token using a secret key
        decoded_token = jwt.decode(token, 'your_secret_key', algorithms=['HS256'])

        # Perform any additional token validation logic here
        # For example, check if the token is expired or validate against a user database

        # Validate the required fields
        if not name:
            return jsonify({'message': 'Category name is required'}), 400

        # Create a new category document
        category = {
            'name': name,
            'created_at': datetime.datetime.now()
        }

        # Insert the category document into the collection
        result = categories_collection.insert_one(category)

        # Return a response indicating the success of the operation
        if result.inserted_id:
            return jsonify({'message': 'Category created successfully', 'category_id': str(result.inserted_id)}), 201
        else:
            return jsonify({'message': 'Failed to create category'}), 500

    except jwt.DecodeError:
        return jsonify({'message': 'Invalid token'}), 401
    



@routes.route('/admin/category/list', methods=['GET'])
def get_categories():
    auth_header = request.headers.get('Authorization')

    if not auth_header:
        return jsonify({'message': 'Token is missing'}), 400

    # Extract the token from the "Bearer <token>" format
    token = auth_header.split(' ')[1]

    try:
        # Verify and decode the token using a secret key
        decoded_token = jwt.decode(token, 'your_secret_key', algorithms=['HS256'])

        # Perform any additional token validation logic here
        # For example, check if the token is expired or validate against a user database

        # Connect to the MongoDB database
        client = MongoClient('mongodb://localhost:27017/')
        db = client['blogs']

        # Retrieve all categories from the collection
        categories_collection = db['category']
        categories = list(categories_collection.find({}, {'_id': 1, 'name': 1}))

        categories_data = [{'category_id': str(category['_id']), 'name': category['name']} for category in categories]

        return jsonify(categories_data), 200

    except jwt.DecodeError:
        return jsonify({'message': 'Invalid token'}), 401