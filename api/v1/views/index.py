#!/usr/bin/python3
"""
Index for V1
"""
from api.v1.views import app_views

@app_views.rout('/status'):
def status_check():
  """
  Returns the status of the api
  """
  status = {'status': 'OK'}
  return (str(status))
