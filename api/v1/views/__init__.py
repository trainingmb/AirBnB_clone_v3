#!/usr/bin/python3
"""
Init for Views in V1
"""
from api.v1.views.index import *
from flask import Blueprint

app_views = Blueprint('api/v1', __name__)
