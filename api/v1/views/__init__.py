#!/usr/bin/python3
"""
Init for Views in V1
"""
from flask import Blueprint, jsonify, abort, request
from api.v1.views.amenities import *
from api.v1.views.cities import *
from api.v1.views.index import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.states import *
from api.v1.views.users import *

app_views = Blueprint('ap_views', __name__, url_prefix="/api/v1")
