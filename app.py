from flask import Flask, abort, jsonify, request
from datetime import datetime
from flask_cors import CORS
from models import setup_db, Actor, Movie
from auth.auth import AuthError, requires_auth


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r'/*': {'origins': '*'}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE')
        return response

    # Actor endpoints
    @app.route('/actors')
    @requires_auth('get:actors')
    def get_all_actors(jwt):
        actors = Actor.query.all()

        return jsonify({
            'success': True,
            'actors': [actor.format() for actor in actors]
        })

    @app.route('/actors/<int:id>')
    @requires_auth('get:actors')
    def get_actor(jwt, id):
        actor = Actor.query.get(id)

        if actor:
            return jsonify({
                'success': True,
                'actor': actor.format()
            })
        else:
            abort(404)

    @app.route('/actors/', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(jwt):
        form = request.get_json()

        name = form.get('name')
        age = form.get('age')
        gender = form.get('gender')
        movies = form.get('movies')

        if not name and not age and not gender and not movies:
            abort(400)

        actor = Actor(name, age, gender)

        if movies:
            for movie_id in form.get('movies'):
                movie = Movie.query.get(movie_id)
                if movie:
                    actor.movies.append(movie)

        try:
            actor.insert()
            return jsonify({
                'success': True,
                'actor': actor.full_details()
            }), 201
        except:
            abort(422)

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(jwt, id):
        form = request.get_json()

        if not form.get('name') and not form.get('age') and not form.get('gender'):
            abort(400)

        actor = Actor.query.get(id)

        if not actor:
            abort(404)

        if form.get('name'):
            actor.name = form.get('name')

        if form.get('age'):
            actor.age = form.get('age')

        if form.get('gender'):
            actor.gender = form.get('gender')

        try:
            actor.update()

            return jsonify({
                'success': True,
                'actor': actor.full_details()
            })
        except:
            abort(422)

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(jwt, id):
        try:
            actor = Actor.query.get(id)
            actor.movies = []
            actor.update()
            actor.delete()

            return jsonify({
                'success': True,
                'deleted_id': actor.id
            })
        except:
            abort(422)

    # Movie endpoints
    @app.route('/movies')
    @requires_auth('get:movies')
    def get_all_movies(jwt):
        movies = Movie.query.all()

        return jsonify({
            'success': True,
            'movies': [movie.format() for movie in movies]
        })

    @app.route('/movies/<int:id>')
    @requires_auth('get:movies')
    def get_movie(jwt, id):
        movie = Movie.query.get(id)

        if not movie:
            abort(404)

        return jsonify({
            'success': True,
            'movie': movie.format()
        })

    @app.route('/movies/', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(jwt):
        form = request.get_json()

        if not form.get('title') or not form.get('release_date'):
            abort(400)

        release_date = datetime.strptime(form.get('release_date'), '%Y-%m-%d')

        movie = Movie(form.get('title'), release_date)

        if form.get('actors'):
            for actor_id in form.get('actors'):
                actor = Actor.query.get(actor_id)
                if actor:
                    movie.movies.append(actor)

        movie.insert()
        # TODO: Check if inserted
        return jsonify({
            'success': True,
            'movie': movie.full_details()
        }), 201

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(jwt, id):
        form = request.get_json()

        if not form.get('title') and not form.get('release_date'):
            abort(400)

        movie = Movie.query.get(id)

        if not movie:
            abort(404)

        if form.get('title'):
            movie.title = form.get('title')

        if form.get('release_date'):
            release_date = datetime.strptime(form.get('release_date'), '%Y-%m-%d')
            movie.release_date = release_date
        try:
            movie.update()

            return jsonify({
                'success': True,
                'movie': movie.full_details()
            })
        except:
            abort(422)

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(jwt, id):
        try:
            movie = Movie.query.get(id)
            movie.actors = []
            movie.update()
            movie.delete()

            return jsonify({
                'success': True,
                'deleted_id': movie.id
            })
        except:
            abort(422)

    # Add/remove actors to/from movies
    @app.route('/movies/<int:movie_id>/actors/<int:actor_id>', methods=['PUT'])
    @requires_auth('patch:movies')
    def add_actor_to_movie(jwt, movie_id, actor_id):
        movie = Movie.query.get(movie_id)
        actor = Actor.query.get(actor_id)

        movie.actors.append(actor)
        movie.update()

        return jsonify({
            'success': True,
            'movie': movie.full_details()
        })

    @app.route('/movies/<int:movie_id>/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('patch:movies')
    def remove_actor_from_movie(jwt, movie_id, actor_id):
        movie = Movie.query.get(movie_id)
        actor = Actor.query.get(actor_id)

        movie.actors.remove(actor)
        movie.update()

        return jsonify({
            'success': True,
            'movie': movie.full_details()
        })

    # Add/remove movies to/from actors
    @app.route('/actors/<int:actor_id>/movies/<int:movie_id>', methods=['PUT'])
    @requires_auth('patch:actors')
    def add_movie_to_actor(jwt, movie_id, actor_id):
        movie = Movie.query.get(movie_id)
        actor = Actor.query.get(actor_id)

        actor.movies.append(movie)
        actor.update()

        return jsonify({
            'success': True,
            'actor': actor.full_details()
        })

    @app.route('/actors/<int:actor_id>/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('patch:actors')
    def remove_movie_from_actors(jwt, movie_id, actor_id):
        movie = Movie.query.get(movie_id)
        actor = Actor.query.get(actor_id)

        actor.movies.remove(movie)
        actor.update()

        return jsonify({
            'success': True,
            'actor': actor.full_details()
        })

    # Error handling
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "page not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "server error"
        }), 500

    @app.errorhandler(AuthError)
    def authorisation_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error
        }), error.status_code

    return app

app = create_app()