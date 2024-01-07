#!/usr/bin/python3
"""
API Base for amenity based actions
"""
from api.v1.views import app_views, jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['POST', 'GET'], strict_slashes=False)
def all_amenities():
  """
  Returns a list of all amenities
  """
  if request.method == 'GET':
    amenities = [i.to_dict() for i in storage.all(Amenity).values()]
    return (jsonify(amenities))
  if request.method == 'POST':
    if not request.is_json:
      abort(400, 'Not a JSON')
    sud = request.get_json()
    if 'name' is not in sud.keys():
      abort(400, 'Missing name')
    newamenity = Amenity(**sud)
    newamenity.save()
    return ((jsonify(newamenity.to_dict()), 201))

@app_views.route('/amenities/<amenity_id>', methods = ['PUT', 'GET', 'DELETE'])
def rud_amenity(amenity_id):
  """
  Get/Modify/Delete amenity with id <amenity_id>
  if present else returns raises error 404
  """
  amenity_obj = storage.get(Amenity, amenity_id)
  if amenity_obj is None:
    abort(404)
  if request.method == 'GET':
    return (jsonify(amenity_obj.to_dict()))
  if request.method == 'PUT':
    if not request.is_json:
      abort(400, 'Not a JSON')
    sud = request.get_json()
    if 'name' not in sud.keys():
      abort(400, 'Missing name')
    for key, value in sud.items():
      if key not in ['id', 'created_at', 'updated_at']:
        setattr(amenity_obj, key, value)
    amenity_obj.save()
    return ((jsonify(amenity_obj.to_dict()), 200))
  if request.method == 'DELETE':
    storage.delete(amenity_obj)
    del amenity_obj
    storage.save()
    return (jsonify({}), 200)
