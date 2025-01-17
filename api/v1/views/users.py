#!/usr/bin/python3
"""
API Base for user based actions
"""
from api.v1.views import app_views, jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['POST', 'GET'], strict_slashes=False)
def all_users():
    """
    Returns a list of all users
    """
    if request.method == 'GET':
        users = [i.to_dict() for i in storage.all(User).values()]
        return (jsonify(users))
    if request.method == 'POST':
        if not request.is_json:
            abort(400, 'Not a JSON')
        sud = request.get_json()
        if 'email' not in sud.keys():
            abort(400, 'Missing email')
        if 'password' not in sud.keys():
            abort(400, 'Missing password')
        newuser_obj = User(**sud)
        newuser_obj.save()
        return (jsonify(newuser_obj.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT', 'GET', 'DELETE'])
def rud_user(user_id):
    """
    Get/Modify/Delete user with id <user_id>
    if present else returns raises error 404
    """
    user_obj = storage.get(User, user_id)
    if user_obj is None:
        abort(404)
    if request.method == 'GET':
        return (jsonify(user_obj.to_dict()))
    if request.method == 'PUT':
        if not request.is_json:
            abort(400, 'Not a JSON')
        sud = request.get_json()
        for key, value in sud.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user_obj, key, value)
        user_obj.save()
        return (jsonify(user_obj.to_dict()), 200)
    if request.method == 'DELETE':
        storage.delete(user_obj)
        del user_obj
        storage.save()
        return (jsonify({}), 200)
