#!/usr/bin/python3
"""
API Base for city based actions
"""
from api.v1.views import app_views, jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['POST', 'GET'],
                 strict_slashes=False)
def city_states(state_id):
    """
    Relates city and states
    """
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    if request.method == 'GET':
        cities_state = [i.to_dict() for i in state_obj.cities]
        return (jsonify(cities_state))
    if request.method == 'POST':
        if not request.is_json:
            abort(400, 'Not a JSON')
        sud = request.get_json()
        if 'name' not in sud.keys():
            abort(400, 'Missing name')
        newcity = City(**sud)
        newcity.state_id = state_obj.id
        newcity.save()
        return (jsonify(newcity.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT', 'GET', 'DELETE'])
def rud_city(city_id):
    """
    Get/Modify/Delete city with id <city_id>
    if present else returns raises error 404
    """
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
    if request.method == 'GET':
        return (jsonify(city_obj.to_dict()))
    if request.method == 'PUT':
        if not request.is_json:
            abort(400, 'Not a JSON')
        sud = request.get_json()
        for key, value in sud.items():
            if key not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city_obj, key, value)
        city_obj.save()
        return (jsonify(city_obj.to_dict()), 200)
    if request.method == 'DELETE':
        storage.delete(city_obj)
        del city_obj
        storage.save()
        return (jsonify({}), 200)
