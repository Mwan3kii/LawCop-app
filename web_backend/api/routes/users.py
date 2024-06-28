#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Users """
from models.user import User
from models import storage
from werkzeug.security import generate_password_hash
from api.routes import app_routes
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_routes.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """
    Retrieves the list of all user objects
    or a specific user
    """
    all_users = storage.all(User)
    list_users = []
    if all_users is None:
        abort(404)
    for user in all_users.values():
        list_users.append(user.to_dict())
    return jsonify(list_users), 200

@app_routes.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """
    Deletes a user Object
    """

    user = storage.get(User, user_id)
    if not user:
        abort(404)
    User.delete()
    storage.save()
    return jsonify({"success": True}), 201


@app_routes.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """
    Creates a user
    """
    data = request.get_json()
    password = data.get("password")
    email = data.get("email")
    username = data.get("username")
    if not email:
        abort(400, description="Email must be provided!")
    if not password:
        abort(400, description="Email must be provided!")
    if len(password) < 5:
        abort(400, description="Weak password, provide a stronger password")
    existing_users = storage.all(User)
    if existing_users:
        for user in existing_users.values():
            if user.email == email:
                abort(409, description="User with that email already exists!")
    new_user = User(email=email, password=generate_password_hash(password, method'pbkdf2:sha256'))
    if username:
        setattr(new_user, 'username', username)
    new_user.save()
    return jsonify(storage.get(User, new_user.id).to_dict()), 201