#!/usr/bin/python3
"""
API Base for state based actions
"""
from api.v1.views import app_views, jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['POST', 'GET'], strict_slashes=False)
def all_states():
    """
    Returns a list of all states
    """
    if request.method == 'GET':
        states = [i.to_dict() for i in storage.all(State).values()]
        return (jsonify(states))
    if request.method == 'POST':
        if not request.is_json:
            abort(400, 'Not a JSON')
        sud = request.get_json()
        if 'name' not in sud.keys():
            abort(400, 'Missing name')
        newstate_obj = State(**sud)
        newstate_obj.save()
        return (jsonify(newstate_obj.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT', 'GET', 'DELETE'])
def rud_state(state_id=None):
    """
    Get/Modify/Delete state with id <state_id>
    if present else returns raises error 404
    """
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    if request.method == 'GET':
        return (jsonify(state_obj.to_dict()))
    if request.method == 'PUT':
        if not request.is_json:
            abort(400, 'Not a JSON')
        sud = request.get_json()
        for key, value in sud.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state_obj, key, value)
        state_obj.save()
        return ((jsonify(state_obj.to_dict()), 200))
    if request.method == 'DELETE':
        storage.delete(state_obj)
        del state_obj
        storage.save()
        return (jsonify({}), 200)
