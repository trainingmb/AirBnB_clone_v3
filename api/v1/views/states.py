#!/usr/bin/python3
"""
Index for V1
"""
from api.v1.views import app_views, jsonify, abort
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models import storage
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

@app_views.route('/states')
def all_states():
  """
  Returns a list of all states
  """
  states = [i.to_dict() for i in storage.all(State).values()]
  return (jsonify(states))

@app_views.route('/states/<state_id>')
def get_state(state_id):
  """
  Return stae with id <state_id>
  if present else returns raises error 404
  """
  print(state_id)
  state_obj = storage.get(State,state_id)
  if state_obj is not None:
    return (jsonify(state_obj.to_dict()))
  abort(404)
