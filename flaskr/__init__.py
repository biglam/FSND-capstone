from flask import Flask, request, abort, jsonify, request
from datetime import datetime
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

  # Movie endpoints
  @app.route('/movies')
  def get_all_movies():
    movies = Movie.query.all()

    return jsonify({
      'success': True,
      'movies': [movie.format() for movie in movies]
    })

  @app.route('/movies/<int:id>')
  def get_movie(id):
    movie = Movie.query.get(id)
    # TODO: check if found
    return jsonify({
      'success': True,
      'movie': movie.format()
    })

  @app.route('/movies/', methods=['POST'])
  def create_movie():
    form = request.get_json()
    # TODO: validate form
    release_date = datetime.strptime(form.get('release_date'), '%Y-%m-%d')
    print(release_date)
    movie = Movie(form.get('title'), release_date)
    movie.insert()
    # TODO: Check if inserted
    return jsonify({
      'success': True,
      'movie': movie.format()
    }), 200

  @app.route('/movies/<int:id>', methods=['PATCH'])
  def update_movie(id):
    form = request.get_json()
    # TODO: Validate form
    movie = Movie.query.get(id)
    # TODO: check movie exists

    if form.get('title'):
      movie.title = form.get('title')

    if form.get('release_date'):
      release_date = datetime.strptime(form.get('release_date'), '%Y-%m-%d')
      movie.release_date = release_date

    movie.update()
    # TODO: Check successfully updated
    return jsonify({
      'success': True,
      'movie': movie.format()
    })

  @app.route('/movies/<int:id>', methods=['DELETE'])
  def delete_movie(id):
    movie = Movie.query.get(id)
    # TODO: check exists

    movie.delete()
    # TODO: check deleted

    return jsonify({
      'success': True,
      'deleted_id': movie.id
    })

  return app