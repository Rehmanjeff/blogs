from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from datetime import datetime, timedelta
from bson.objectid import ObjectId
import bcrypt
import main
import jwt
import re
import os

UPLOAD_FOLDER = '../frontend/public/assets/authors'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_secret_key():
    return 'your_secret_key'

def get_algorithem():
    return 'HS256'

def get_refresh_secret_key():
    return 'your_refresh_token_secret_key'

def get_database():
    client = MongoClient('mongodb://localhost:27017/')
    return client['blogs']

def get_authenticated_user():

    access_token = request.headers.get('Authorization')
    secret_key = get_secret_key() 
    algorithm = get_algorithem()

    try:
        payload = jwt.decode(access_token, secret_key, algorithms=[algorithm])
        email = payload.get('email')

        db = get_database()
        users_collection = db['users']

        user = users_collection.find_one({'email': email, 'access_token': access_token})

        if not user:
            return None
        else:
            return user
    except jwt.ExpiredSignatureError:
        return None 
    except jwt.InvalidTokenError:
        return None

routes = Blueprint('routes', __name__)

@routes.route('/scrape', methods=['POST'])
def scrapeUrl():
    data = request.get_json()
    result = main.scrape(data)
    return result

@routes.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name :
        return jsonify({'message': 'Please provide your name'}), 400
    if not email:
        return jsonify({'message':'Please provide your email'}), 400
    if not password:
        return jsonify({'message':'Please provide your password'}), 400
    
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        return jsonify({'message': 'Invalid email address'}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    db = get_database()
    users_collection = db['users']

    user = {
        'name': name,
        'email': email,
        'password': hashed_password.decode('utf-8'),
    }
    result = users_collection.insert_one(user)

    if result.inserted_id:
        return jsonify({'message': 'User registered successfully'})
    
    else:
        return jsonify({'message': 'Failed to register user'})
    
@routes.route('/admin/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email:
        return jsonify({'message':'Please provide email'}), 400

    if not password:
        return jsonify({'message': 'Please provide  password'}), 400

    db = get_database()
    users_collection = db['users']

    user = users_collection.find_one({'email': email})

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        
        expiration_time = datetime.utcnow() + timedelta(days=7)
        payload = {'email': email, 'exp': expiration_time}
        secret_key = get_secret_key()
        algorithm = get_algorithem()
        access_token = jwt.encode(payload, secret_key, algorithm = algorithm)

        refresh_token_payload = {'email': email}
        refresh_token_secret_key = get_refresh_secret_key()
        refresh_token_algorithm = get_algorithem()
        refresh_token = jwt.encode(refresh_token_payload, refresh_token_secret_key, algorithm=refresh_token_algorithm)

        users_collection.update_one({'_id': user['_id']}, {'$set': {'access_token': access_token}})
        users_collection.update_one({'_id': user['_id']}, {'$set': {'refresh_token': refresh_token}})

        return jsonify({'message': 'Login successful','user_id': str(user['_id']), 'access_token': access_token, 'refresh_token':refresh_token})
    else:
        return jsonify({'message': 'Invalid credentials'}), 401  
    
@routes.route('/admin/dashboard', methods=['GET'])
def admin_dashboard():
    
    user = get_authenticated_user()

    return jsonify({'user': str(user['_id'])}), 200
    
@routes.route('/admin/refresh', methods=['POST'])
def refresh_token():
    data = request.get_json()
    refresh_token = data.get('refresh_token')

    if not refresh_token:
        return jsonify({'message': 'Refresh token is missing'}), 401

    refresh_token_secret_key = get_refresh_secret_key()
    refresh_token_algorithm = get_algorithem()
    try:
        payload = jwt.decode(refresh_token, refresh_token_secret_key, algorithms=[refresh_token_algorithm])
        email = payload.get('email')

        expiration_time = datetime.utcnow() + datetime.timedelta(days=7)
        access_token_payload = {'email': email, 'exp': expiration_time}
        secret_key = get_secret_key()
        algorithm = get_algorithem()
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
            secret_key = get_secret_key()
            payload = jwt.decode(access_token, secret_key, algorithms=[get_algorithem()])
            email = payload['email']

            db = get_database()
            users_collection = db['users']
            user = users_collection.find_one({'email': email})

            if user:
                user['access_token'] = None
                user['refresh_token'] = None
                users_collection.update_one({'_id': user['_id']}, {'$set': user})

                return jsonify({'message': 'Logout successful'})

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Access token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid access token'}), 401

    return jsonify({'message': 'Invalid authorization header'}), 401

@routes.route('/admin/authors', methods=['POST'])
def create_author():
    
    name = request.form.get('name')

    if not name:
        return jsonify({'error': 'Name is required'}), 400

    if 'avatar' not in request.files:
        return jsonify({'error': 'Avatar image is required'}), 400

    avatar_file = request.files['avatar']

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    if avatar_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not allowed_file(avatar_file.filename):
        return jsonify({'error': 'Invalid file extension'}), 400

    filename = secure_filename(avatar_file.filename)

    avatar_path = os.path.join(UPLOAD_FOLDER, filename)
    avatar_file.save(avatar_path)

    author = {
        'name': name,
        'avatar': filename,
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    db = get_database()
    authors_collection = db['authors']
    result = authors_collection.insert_one(author)

    if result.inserted_id:
        return jsonify({'message': 'Author created successfully'}), 201
    else:
        return jsonify({'message': 'Failed to create author'}), 400

@routes.route('/admin/authors/<id>', methods=['PUT'])
def update_author(id):

    db = get_database()
    authors_collection = db['authors']
    name = request.form.get('name')

    if not name:
        return jsonify({'error': 'Name is required'}), 400
    
    author = authors_collection.find_one({'_id': ObjectId(id)})
    
    if not author:
        return jsonify({'error': 'Target object not found'}), 400
    
    if 'avatar' in request.files:
        
        avatar_file = request.files['avatar']

        if author['avatar']:
            existing_avatar_path = os.path.join(UPLOAD_FOLDER, author['avatar'])
            if os.path.exists(existing_avatar_path):
                os.remove(existing_avatar_path)

        filename = secure_filename(avatar_file.filename)
        avatar_path = os.path.join(UPLOAD_FOLDER, filename)
        avatar_file.save(avatar_path)

        authors_collection.update_one({'_id': ObjectId(id)}, {'$set': {'avatar': filename, 'name' : name}})
    else:
        authors_collection.update_one({'_id': ObjectId(id)}, {'$set': {'name' : name}})
    
    return jsonify({'message': 'Author updated successfully'}), 200
    
@routes.route('/admin/authors', methods=['GET'])
def list_authors():
    
    db = get_database()
    authors_collection = db['authors']

    authors = authors_collection.find()

    author_list = []
    for author in authors:

        db_datetime = datetime.strptime(author['created_at'], "%Y-%m-%d %H:%M:%S")
        formatted_datetime = db_datetime.strftime("%d-%m-%Y %H:%M:%S")
        author_data = {
            'id': str(author['_id']),
            'name': author['name'],
            'avatar': author['avatar'],
            'created_at': formatted_datetime
        }
        author_list.append(author_data)

    return jsonify({'authors': author_list}), 200

@routes.route('/admin/category', methods=['POST'])
def create_category():
    
    data = request.get_json()
    name = data.get('name')
    db = get_database()

    categories_collection = db['category']

    try:
        if not name:
            return jsonify({'message': 'Category name is required'}), 400

        category = {
            'name': name,
            'created_at': datetime.now()
        }

        result = categories_collection.insert_one(category)

        if result.inserted_id:
            return jsonify({'message': 'Category created successfully', 'category_id': str(result.inserted_id)}), 201
        else:
            return jsonify({'message': 'Failed to create category'}), 500

    except jwt.DecodeError:
        return jsonify({'message': 'Invalid token'}), 401
    
@routes.route('/admin/category/list', methods=['GET'])
def get_categories():
    
    try:
        
        db = get_database()
        categories_collection = db['category']
        categories = list(categories_collection.find({}, {'_id': 1, 'name': 1}))
        categories_data = [{'category_id': str(category['_id']), 'name': category['name']} for category in categories]

        return jsonify(categories_data), 200

    except jwt.DecodeError:
        return jsonify({'message': 'Invalid token'}), 401