#!/usr/bin/python3
"""
API Base for place reviews based actions
"""
from api.v1.views import app_views, jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.state import State


@app_views.route('/places/<place_id>/reviews', methods=['POST', 'GET'], strict_slashes=False)
def places_reviews(place_id):
  """
  Returns a list of all place reviews
  """
  place_obj = storage.get(Place,place_id)
  if place_obj is None:
    abort(404)
  if request.method == 'GET':
    reviews = [i.to_dict() for i in place_obj.reviews]
    return (jsonify(reviews))
  if request.method == 'POST':
    if not request.is_json:
      abort(400, 'Not a JSON')
    sud = request.get_json()
    if 'user_id' not in sud.keys():
      abort(400, 'Missing user_id')
    else:
      user_obj = storage.get(User, sud['user_id'])
      if user_obj is None:
        abort(404)
    if 'text' not in sud.keys():
      abort(400, 'Missing text')
    sud['place_id'] = place_obj.id
    newreview_obj = Review(**sud)
    newreview_obj.save()
    return (jsonify(newreview_obj.to_dict()), 201)

@app_views.route('/reviews/<review_id>', methods=['PUT', 'GET', 'DELETE'])
def rud_review(review_id):
  """
  Get/Modify/Delete review with id <review_id>
  if present else returns raises error 404
  """
  review_obj = storage.get(Review,review_id)
  if review_obj is None:
    abort(404)
  if request.method == 'GET':
    return (jsonify(review_obj.to_dict()))
  if request.method == 'PUT':
    if not request.is_json:
      return abort(400, 'Not a JSON')
    sud = request.get_json()
    for key, value in sud.items():
      if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
        setattr(review_obj, key, value)
    review_obj.save()
    return (jsonify(review_obj.to_dict()), 200)
  if request.method == 'DELETE':
    storage.delete(review_obj)
    del review_obj
    storage.save()
    return (jsonify({}), 200)
