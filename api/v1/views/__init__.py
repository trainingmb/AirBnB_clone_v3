#!/usr/bin/python3
"""
Init for Views in V1
"""
from flask import Blueprint, jsonify, abort, request

app_views = Blueprint('ap_views', __name__, url_prefix="/api/v1")

from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
