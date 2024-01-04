#!/usr/bin/python3
"""Version 1 Flask App"""
from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
  """
  Closes the storage on teardown
  """
  storage.close()


if __name__ == '__main__':
  from api.v1 import HBNB_API_HOST, HBNB_API_PORT
  app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
