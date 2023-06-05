from flask import Flask
from routes import routes, get_secret_key, get_algorithem, get_database
from flask_cors import CORS
from flask import request, jsonify
import jwt
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)
app.register_blueprint(routes)
app.debug = True

def authorize_user():
    
    access_token = request.headers.get('Authorization')

    if not access_token:
        return jsonify({'message': 'Access token is missing'}), 401

    secret_key = get_secret_key() 
    algorithm = get_algorithem()
    try:
        payload = jwt.decode(access_token, secret_key, algorithms=[algorithm])
        email = payload.get('email')

        db = get_database()
        users_collection = db['users']

        user = users_collection.find_one({'email': email, 'access_token': access_token})

        if not user:
            return jsonify({'message': "Token dosen't exists in database"}), 401
        else:
            return None
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Access token has expired'}), 401 
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid refresh token'}), 401

@app.before_request
def before_request_func():
    
    if request.endpoint in ['routes.create_author', 'routes.update_author', 'routes.admin_dashboard', 'routes.list_authors', 'routes.create_category', 'routes.get_categories', 'routes.update_category']:
        
        if request.method == 'OPTIONS':
            
            response = app.make_default_options_response()
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
        else:
            # Handle actual requests
            response = authorize_user()
        return response
    
if __name__ == '__main__':
    app.run(debug=True)