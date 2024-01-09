#!/usr/bin/python3
"""
API Base for place reviews based actions
"""
from api.v1.views import app_views, jsonify, abort, request
import models
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'],
                 strict_slashes=False)
def places_amenities(place_id):
    """
    Returns a list of all place reviews
    """
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)
    if request.method == 'GET':
        amenities = [i.to_dict() for i in place_obj.amenities]
        return (jsonify(amenities))


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST', 'DELETE'])
def rud_place_amenity(place_id, amenity_id):
    """
    Link/Delete amenity from place
    if present else returns raises error 404
    """
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        abort(404)
    if request.method == 'POST':
        if amenity_obj in place_obj.amenities:
            return (jsonify(amenity_obj.to_dict()), 200)
        if models.storage_t != 'db':
            setattr(amenity_obj, 'place_id', place_obj.id)
            amenity_obj.save()
        else:
            place_obj.amenities.append(amenity_obj)
            place_obj.save()
        return (jsonify(amenity_obj.to_dict()), 201)
    if request.method == 'DELETE':
        if amenity_obj not in place_obj.amenities:
            abort(404)
        if models.storage_t != 'db':
            setattr(amenity_obj, 'place_id', '')
            amenity_obj.save()
        else:
            place_obj.amenities.remove(amenity_obj)
            place_obj.save()
        return (jsonify({}), 200)
