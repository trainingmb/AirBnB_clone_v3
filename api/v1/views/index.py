#!/usr/bin/python3
"""
Index for V1
"""
from api.v1.views import app_views, jsonify
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

@app_views.route('/status')
def status_check():
  """
  Returns the status of the api
  """
  status = {'status': 'OK'}
  return (jsonify(status))

@app_views.route('/stats')
def cls_stats():
  """
  Return the JSON statistics
  for all classes
  """
  cls = {'amenities': storage.count(Amenity),
         'cities': storage.count(City),
         'places': storage.count(Place),
         'reviews': storage.count(Review),
         'states': storage.count(State),
         'users': storage.count(User)
        }
  return (jsonify(cls))
