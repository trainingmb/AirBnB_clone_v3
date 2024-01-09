#!/usr/bin/python3
"""
API Base for place based actions
"""
from api.v1.views import app_views, jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['POST', 'GET'],
                 strict_slashes=False)
def all_places(city_id):
    """
    Returns a list of all states
    """
    city_obj = storage.get(City,city_id)
    if city_obj is None:
        abort(404)
    if request.method == 'GET':
        places = [i.to_dict() for i in city_obj.places]
        return (jsonify(places))
    if request.method == 'POST':
        if not request.is_json:
            abort(400, 'Not a JSON')
        sud = request.get_json()
        if 'user_id' not in sud.keys():
            abort(400, 'Missing user_id')
        else:
            user_obj = storage.get(User,user_id)
            if user_obj is None:
                abort(404)
        if 'name' not in sud.keys():
            abort(400, 'Missing name')
        newplace_obj = Place(**sud)
        newplace_obj.city_id = city_obj.id
        newplace_obj.save()
        return (jsonify(newplace_obj.to_dict()), 201)


@app_views.route('/places/<place_id>',
                 methods=['PUT', 'GET', 'DELETE'],
                 strict_slashes=False)
def rud_place(state_id):
    """
    Get/Modify/Delete place with id <place_id>
    if present else returns raises error 404
    """
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)
    if request.method == 'GET':
        return (jsonify(place_obj.to_dict()))
    if request.method == 'PUT':
        if not request.is_json:
            abort(400, 'Not a JSON')
        sud = request.get_json()
        for key, value in sud.items():
            if key not in ['id', 'user_id', 'created_at', 'updated_at']:
                setattr(place_obj, key, value)
        place_obj.save()
        return (jsonify(place_obj.to_dict()), 200)
    if request.method == 'DELETE':
        storage.delete(place_obj)
        del place_obj
        storage.save()
        return (jsonify({}), 200)
