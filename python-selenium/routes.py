from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from datetime import datetime, timedelta
from bson.objectid import ObjectId
from bson import ObjectId
import bcrypt
import json
import main
import jwt
import re
import os
from flask import Flask, jsonify

UPLOAD_FOLDER = "../frontend/public/assets/authors"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_secret_key():
    return "your_secret_key"


def get_algorithem():
    return "HS256"


def get_refresh_secret_key():
    return "your_refresh_token_secret_key"


def get_database():
    client = MongoClient("mongodb://localhost:27017/")
    return client["blogs"]


def get_authenticated_user():
    access_token = request.headers.get("Authorization")
    secret_key = get_secret_key()
    algorithm = get_algorithem()

    try:
        payload = jwt.decode(access_token, secret_key, algorithms=[algorithm])
        email = payload.get("email")

        db = get_database()
        users_collection = db["users"]

        user = users_collection.find_one({"email": email, "access_token": access_token})

        if not user:
            return None
        else:
            return user
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def create_slug(text):
    if not isinstance(text, str):
        return None

    slug = re.sub(r"[^a-zA-Z0-9\s-]", "", text)
    slug = re.sub(r"\s+", "-", slug).strip()
    slug = slug.lower()

    return slug


routes = Blueprint("routes", __name__)


@routes.route("/scrape", methods=["POST"])
def scrapeUrl():
    data = request.get_json()
    result = main.scrape(data)
    return result


@routes.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name:
        return jsonify({"message": "Please provide your name"}), 400
    if not email:
        return jsonify({"message": "Please provide your email"}), 400
    if not password:
        return jsonify({"message": "Please provide your password"}), 400

    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
        return jsonify({"message": "Invalid email address"}), 400

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    db = get_database()
    users_collection = db["users"]

    user = {
        "name": name,
        "email": email,
        "password": hashed_password.decode("utf-8"),
    }
    result = users_collection.insert_one(user)

    if result.inserted_id:
        return jsonify({"message": "User registered successfully"})

    else:
        return jsonify({"message": "Failed to register user"})


@routes.route("/admin/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email:
        return jsonify({"message": "Please provide email"}), 400

    if not password:
        return jsonify({"message": "Please provide  password"}), 400

    db = get_database()
    users_collection = db["users"]

    user = users_collection.find_one({"email": email})

    if user and bcrypt.checkpw(
        password.encode("utf-8"), user["password"].encode("utf-8")
    ):
        expiration_time = datetime.utcnow() + timedelta(days=7)
        payload = {"email": email, "exp": expiration_time}
        secret_key = get_secret_key()
        algorithm = get_algorithem()
        access_token = jwt.encode(payload, secret_key, algorithm=algorithm)

        refresh_token_payload = {"email": email}
        refresh_token_secret_key = get_refresh_secret_key()
        refresh_token_algorithm = get_algorithem()
        refresh_token = jwt.encode(
            refresh_token_payload,
            refresh_token_secret_key,
            algorithm=refresh_token_algorithm,
        )

        users_collection.update_one(
            {"_id": user["_id"]}, {"$set": {"access_token": access_token}}
        )
        users_collection.update_one(
            {"_id": user["_id"]}, {"$set": {"refresh_token": refresh_token}}
        )

        return jsonify(
            {
                "message": "Login successful",
                "user_id": str(user["_id"]),
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
        )
    else:
        return jsonify({"message": "Invalid credentials"}), 401


@routes.route("/admin/dashboard", methods=["GET"])
def admin_dashboard():
    user = get_authenticated_user()

    return jsonify({"user": str(user["_id"])}), 200


@routes.route("/admin/refresh", methods=["POST"])
def refresh_token():
    data = request.get_json()
    refresh_token = data.get("refresh_token")

    if not refresh_token:
        return jsonify({"message": "Refresh token is missing"}), 401

    refresh_token_secret_key = get_refresh_secret_key()
    refresh_token_algorithm = get_algorithem()
    try:
        payload = jwt.decode(
            refresh_token,
            refresh_token_secret_key,
            algorithms=[refresh_token_algorithm],
        )
        email = payload.get("email")

        expiration_time = datetime.utcnow() + datetime.timedelta(days=7)
        access_token_payload = {"email": email, "exp": expiration_time}
        secret_key = get_secret_key()
        algorithm = get_algorithem()
        access_token = jwt.encode(access_token_payload, secret_key, algorithm=algorithm)

        return jsonify(
            {"message": "Access token refreshed", "access_token": access_token}
        )
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Refresh token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid refresh token"}), 401


@routes.route("/admin/logout", methods=["POST"])
def logout():
    auth_header = request.headers.get("Authorization")

    if auth_header and auth_header.startswith("Bearer "):
        access_token = auth_header.split(" ")[1]

        # Decode the access token
        try:
            secret_key = get_secret_key()
            payload = jwt.decode(
                access_token, secret_key, algorithms=[get_algorithem()]
            )
            email = payload["email"]

            db = get_database()
            users_collection = db["users"]
            user = users_collection.find_one({"email": email})

            if user:
                user["access_token"] = None
                user["refresh_token"] = None
                users_collection.update_one({"_id": user["_id"]}, {"$set": user})

                return jsonify({"message": "Logout successful"})

        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Access token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid access token"}), 401

    return jsonify({"message": "Invalid authorization header"}), 401


@routes.route("/admin/authors", methods=["POST"])
def create_author():
    name = request.form.get("name")
    designation = request.form.get("designation")

    if not name:
        return jsonify({"error": "Name is required"}), 400

    if "avatar" not in request.files:
        return jsonify({"error": "Avatar image is required"}), 400

    avatar_file = request.files["avatar"]

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    if avatar_file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if not allowed_file(avatar_file.filename):
        return jsonify({"error": "Invalid file extension"}), 400

    filename = secure_filename(avatar_file.filename)

    avatar_path = os.path.join(UPLOAD_FOLDER, filename)
    avatar_file.save(avatar_path)

    author = {
        "name": name,
        "avatar": filename,
        "designation": designation,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    db = get_database()
    authors_collection = db["authors"]
    result = authors_collection.insert_one(author)

    if result.inserted_id:
        return jsonify({"message": "Author created successfully"}), 201
    else:
        return jsonify({"message": "Failed to create author"}), 400


@routes.route("/admin/authors/<id>", methods=["PUT"])
def update_author(id):
    db = get_database()
    authors_collection = db["authors"]
    name = request.form.get("name")
    designation = request.form.get("designation")

    if not name:
        return jsonify({"error": "Name is required"}), 400

    author = authors_collection.find_one({"_id": ObjectId(id)})

    if not author:
        return jsonify({"error": "Target object not found"}), 400

    if "avatar" in request.files:
        avatar_file = request.files["avatar"]

        if author["avatar"]:
            existing_avatar_path = os.path.join(UPLOAD_FOLDER, author["avatar"])
            if os.path.exists(existing_avatar_path):
                os.remove(existing_avatar_path)

        filename = secure_filename(avatar_file.filename)
        avatar_path = os.path.join(UPLOAD_FOLDER, filename)
        avatar_file.save(avatar_path)

        authors_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"avatar": filename, "name": name, "designation": designation}},
        )
    else:
        authors_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": {"name": name, "designation": designation}}
        )

    return jsonify({"message": "Author updated successfully"}), 200


@routes.route("/admin/authors", methods=["GET"])
def list_authors():
    db = get_database()
    authors_collection = db["authors"]

    authors = authors_collection.find()

    author_list = []
    for author in authors:
        db_datetime = datetime.strptime(author["created_at"], "%Y-%m-%d %H:%M:%S")
        formatted_datetime = db_datetime.strftime("%d-%m-%Y %H:%M:%S")
        author_data = {
            "id": str(author["_id"]),
            "name": author["name"],
            "designation": author.get("designation"),
            "avatar": author["avatar"],
            "created_at": formatted_datetime,
        }
        author_list.append(author_data)

    return jsonify({"authors": author_list}), 200


@routes.route("/admin/category", methods=["POST"])
def create_category():
    data = request.get_json()
    name = data.get("name")
    db = get_database()

    categories_collection = db["category"]

    try:
        if not name:
            return jsonify({"message": "Category name is required"}), 400

        category = {"name": name, "created_at": datetime.now()}

        result = categories_collection.insert_one(category)

        if result.inserted_id:
            return (
                jsonify(
                    {
                        "message": "Category created successfully",
                        "category_id": str(result.inserted_id),
                    }
                ),
                201,
            )
        else:
            return jsonify({"message": "Failed to create category"}), 500

    except jwt.DecodeError:
        return jsonify({"message": "Invalid token"}), 401


@routes.route("/admin/category/list", methods=["GET"])
def get_categories():
    try:
        db = get_database()
        categories_collection = db["category"]
        categories = list(categories_collection.find({}, {"_id": 1, "name": 1}))
        categories_data = [
            {"category_id": str(category["_id"]), "name": category["name"]}
            for category in categories
        ]

        return jsonify(categories_data), 200

    except jwt.DecodeError:
        return jsonify({"message": "Invalid token"}), 401


@routes.route("/admin/blogs", methods=["POST"])
def create_blog():
    author_id = request.form.get("author")
    category_id = request.form.get("category")
    type = request.form.get("type")
    status = request.form.get("status")

    if not category_id:
        return jsonify({"error": "Category is required"}), 400
    if not author_id:
        return jsonify({"error": "Author is required"}), 400

    db = get_database()
    categories_collection = db["category"]
    authors_collection = db["authors"]
    category = categories_collection.find_one({"_id": ObjectId(category_id)})
    author = authors_collection.find_one({"_id": ObjectId(author_id)})

    if not category:
        return jsonify({"error": "Category not found"}), 400
    if not author:
        return jsonify({"error": "Author not found"}), 400

    blogPost = {
        "type": type,
        "author": ObjectId(author_id),
        "category": ObjectId(category_id),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": status,
    }

    if type == "link":
        data = {"url": request.form.get("link")}
        result = main.scrape(data)
        if "title" in result:
            blogPost["link"] = request.form.get("link")
            blogPost["name"] = result["title"]
            blogPost["slug"] = create_slug(result["title"])
            blogPost["description"] = result["description"]
        else:
            return jsonify({"message": result}), 400
    elif type == "manual":
        blog_name = request.form.get("name")
        blogPost["name"] = blog_name
        blogPost["slug"] = create_slug(blog_name)
        blogPost["description"] = request.form.get("description")
    else:
        return jsonify({"message": "Type unknown"}), 400

    blogs_collection = db["blog_posts"]
    result = blogs_collection.insert_one(blogPost)

    if result.inserted_id:
        return jsonify({"message": "Blog created successfully"}), 201
    else:
        return jsonify({"message": "Failed to create blog"}), 400


@routes.route("/admin/blogs/<id>", methods=["PUT"])
def update_blog(id):
    db = get_database()
    blogs_collection = db["blog_posts"]
    title = request.form.get("name")
    author_id = request.form.get("author")
    category_id = request.form.get("category")
    description = request.form.get("description")
    status = request.form.get("status")

    if not title:
        return jsonify({"error": "Title is required"}), 400
    if not category_id:
        return jsonify({"error": "Category is required"}), 400
    if not author_id:
        return jsonify({"error": "Author is required"}), 400

    db = get_database()
    categories_collection = db["category"]
    authors_collection = db["authors"]
    category = categories_collection.find_one({"_id": ObjectId(category_id)})
    author = authors_collection.find_one({"_id": ObjectId(author_id)})
    blogPost = blogs_collection.find_one({"_id": ObjectId(id)})

    if not blogPost:
        return jsonify({"error": "Blog not found"}), 400
    if not category:
        return jsonify({"error": "Category not found"}), 400
    if not author:
        return jsonify({"error": "Author not found"}), 400
    if not blogPost:
        return jsonify({"error": "Target object not found"}), 400

    blogs_collection.update_one(
        {"_id": ObjectId(id)},
        {
            "$set": {
                "name": title,
                "slug": create_slug(title),
                "description": description,
                "status": status,
                "category": ObjectId(category_id),
                "author": ObjectId(author_id),
            }
        },
    )

    return jsonify({"message": "Blog updated successfully"}), 200


@routes.route("/admin/blogs/<id>", methods=["GET"])
def read_blog(id):
    db = get_database()
    blogs_collection = db["blog_posts"]
    categories_collection = db["category"]
    authors_collection = db["authors"]

    blogPost = blogs_collection.find_one({"_id": ObjectId(id)})
    if not blogPost:
        return jsonify({"error": "Blog not found"}), 400

    category = categories_collection.find_one({"_id": ObjectId(blogPost["category"])})
    author = authors_collection.find_one({"_id": ObjectId(blogPost["author"])})
    if not category:
        category = {"name": "unknown"}
    if not author:
        author = {"name": "unknown"}

    db_datetime = datetime.strptime(blogPost["created_at"], "%Y-%m-%d %H:%M:%S")
    formatted_datetime = db_datetime.strftime("%d-%m-%Y %H:%M:%S")
    blog = {
        "id": str(blogPost["_id"]),
        "name": blogPost["name"],
        "description": blogPost["description"],
        "status": blogPost["status"],
        "category": str(category["_id"]),
        "author": str(author["_id"]),
        "created_at": formatted_datetime,
    }

    return jsonify({"blog": blog}), 200


@routes.route("/admin/blogs", methods=["GET"])
def list_blogs():
    db = get_database()
    blogs_collection = db["blog_posts"]
    categories_collection = db["category"]
    authors_collection = db["authors"]

    blogPosts = blogs_collection.find()

    blogs = []
    for blogPost in blogPosts:
        db_datetime = datetime.strptime(blogPost["created_at"], "%Y-%m-%d %H:%M:%S")
        formatted_datetime = db_datetime.strftime("%d-%m-%Y %H:%M:%S")

        category = categories_collection.find_one(
            {"_id": ObjectId(blogPost["category"])}
        )
        author_id = blogPost["author"]
        author = authors_collection.find_one({"_id": ObjectId(author_id)})

        designation = author.get("designation")

        author_data = {
            "name": author["name"],
            "avatar": author["avatar"],
            "designation": designation,
        }

        blog_data = {
            "id": str(blogPost["_id"]),
            "name": blogPost["name"],
            "slug": create_slug(blogPost["name"]),
            "description": blogPost["description"],
            "status": blogPost["status"],
            "category": category["name"],
            "author": author_data,
            "created_at": formatted_datetime,
        }
        blogs.append(blog_data)

    return jsonify({"blogs": blogs}), 200


@routes.route("/admin/categories/<category_id>", methods=["PUT"])
def update_category(category_id):
    data = request.get_json()

    db = get_database()
    categories_collection = db["category"]

    try:
        name = data.get("name")
        if not name:
            return jsonify({"message": "Category name is required"}), 400

        update_query = {"$set": {"name": name}}

        result = categories_collection.update_one(
            {"_id": ObjectId(category_id)}, update_query
        )

        if result.modified_count > 0:
            return jsonify({"message": "Category updated successfully"}), 200
        else:
            return jsonify({"message": "Failed to update category"}), 500

    except jwt.DecodeError:
        return jsonify({"message": "Invalid token"}), 401


@routes.route("/blogs/<slug>", methods=["GET"])
def get_blog_by_slug(slug):
    db = get_database()
    blog_collection = db["blog_posts"]
    categories_collection = db["category"]
    authors_collection = db["authors"]
    blogPost = blog_collection.find_one({"slug": slug})
    if not blogPost:
        return jsonify({"message": "Blog not found"}), 404

    category = categories_collection.find_one({"_id": ObjectId(blogPost["category"])})
    author = authors_collection.find_one({"_id": ObjectId(blogPost["author"])})
    if not category:
        category = {"name": "unknown"}
    if not author:
        author = {"name": "unknown"}

    db_datetime = datetime.strptime(blogPost["created_at"], "%Y-%m-%d %H:%M:%S")
    formatted_datetime = db_datetime.strftime("%d-%m-%Y %H:%M:%S")

    designation = author.get("designation")

    blog = {
        "id": str(blogPost["_id"]),
        "name": blogPost["name"],
        "description": blogPost["description"],
        "status": blogPost["status"],
        "category": {"id": str(category["_id"]), "name": category["name"]},
        "author": {
            "id": str(author["_id"]),
            "name": author["name"],
            "avatar": author["avatar"],
            "designation": designation,
        },
        "created_at": formatted_datetime,
    }

    return jsonify({"blog": blog}), 200


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)


@routes.route("/blogs/recent", methods=["GET"])
def get_recent_blogs():
    db = get_database()
    blog_collection = db["blog_posts"]
    author_collection = db["authors"]

    recent_blogs = blog_collection.find().sort("created_at", -1).limit(3)

    blogs = []
    for blog in recent_blogs:
        blog["_id"] = str(blog["_id"])

        author_id = blog.get("author")
        author = author_collection.find_one({"_id": author_id})
        if author:
            blog["author"] = {
                "name": author.get("name"),
                "avatar": author.get("avatar"),
                "designation": author.get("designation"),
            }
        blogs.append(blog)

    return JSONEncoder().encode(blogs), 200


@routes.route("/blogs/recommend", methods=["GET"])
def get_blogs_by_category():
    db = get_database()
    blogs_collection = db["blog_posts"]
    category_collection = db["category"]
    author_collection = db["authors"]
    category_name = request.args.get("category")

    # Find the category document based on the category name
    category = category_collection.find_one({"name": category_name})

    if not category:
        return jsonify({"message": "Category name not valid"}), 400

    if category:
        category_id = category["_id"]
        category_name = category[
            "name"
        ]  # Get the category name from the category document

        # Find the blogs with the matching category ID, limit to 3 and sort by created_at
        blogs = (
            blogs_collection.find({"category": category_id})
            .sort("created_at", -1)
            .limit(3)
        )

        # Prepare the blogs response
        response = []
        for blog in blogs:
            blog["_id"] = str(blog["_id"])

            author_id = blog.get("author")
            author = author_collection.find_one({"_id": author_id})
            if author:
                blog["author"] = {
                    "name": author.get("name"),
                    "avatar": author.get("avatar"),
                    "designation": author.get("designation"),
                }
            blog[
                "category"
            ] = category_name  # Include the category name in the blog document
            response.append(blog)

        return JSONEncoder().encode(response), 200
    else:
        return jsonify([]), 200
