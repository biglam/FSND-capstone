from flask import Flask, request, abort, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from models import setup_db, Actor, Movie

def create_app(test_config=None):
  app = Flask(__name__)
  setup_db(app)


# Actor endpoints
  @app.route('/actors')
  def get_all_actors():
    actors = Actor.query.all()

    return jsonify({
      'success': True,
      'actors':  [actor.format() for actor in actors]
    })

  @app.route('/actors/<int:id>')
  def get_actor(id):
    actor = Actor.query.get(id)
    #TODO: check if found
    return jsonify({
      'success': True,
      'actor': actor.format()
    })

  @app.route('/actors/', methods=['POST'])
  def create_actor():
    form = request.get_json()
    #TODO: validate form
    actor = Actor(form.get('name'), form.get('age'), form.get('gender'))
    actor.insert()
    #TODO: Check if inserted
    return jsonify({
      'success': True,
      'actor': actor.format()
    }), 200

  @app.route('/actors/<int:id>', methods=['PATCH'])
  def update_actor(id):
    form = request.get_json()
    # TODO: Validate form
    actor = Actor.query.get(id)
    # TODO: check actor exists

    if form.get('name'):
      actor.name = form.get('name')

    if form.get('age'):
      actor.age = form.get('age')

    if form.get('gender'):
      actor.gender = form.get('gender')

    actor.update()
    # TODO: Check successfully updated
    return jsonify({
      'success': True,
      'actor': actor.format()
    })

  @app.route('/actors/<int:id>', methods=['DELETE'])
  def delete_actor(id):
    actor = Actor.query.get(id)
    # TODO: check exists

    actor.delete()
    # TODO: check deleted

    return jsonify({
      'success': True,
      'deleted_id': actor.id
    })

  return app