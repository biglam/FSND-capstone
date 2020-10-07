from flask import Flask, request, abort, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from models import setup_db, Actor, Movie

def create_app(test_config=None):
  app = Flask(__name__)
  setup_db(app)

  @app.route('/')
  def test():
    actors = Actor.query.all()
    print actors
    return 'Foo'

  return app