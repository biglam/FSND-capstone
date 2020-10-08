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
            'actors': [actor.format() for actor in actors]
        })

    @app.route('/actors/<int:id>')
    def get_actor(id):
        actor = Actor.query.get(id)

        if actor:
            return jsonify({
                'success': True,
                'actor': actor.format()
            })
        else:
            abort(404)

    @app.route('/actors/', methods=['POST'])
    def create_actor():
        form = request.get_json()

        name = form.get('name')
        age = form.get('age')
        gender = form.get('gender')
        movies = form.get('movies')

        if not name and not age and not gender and not movies:
            abort(400)

        actor = Actor(name, age, gender)

        if (movies):
            for movie_id in form.get('movies'):
                movie = Movie.query.get(movie_id)
                if movie:
                    actor.movies.append(movie)

        try:
            actor.insert()
            return jsonify({
                'success': True,
                'actor': actor.format()
            }), 201
        except:
            abort(422)

    @app.route('/actors/<int:id>', methods=['PATCH'])
    def update_actor(id):
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
                'actor': actor.format()
            })
        except:
            abort(422)

    @app.route('/actors/<int:id>', methods=['DELETE'])
    def delete_actor(id):
        try:
            actor = Actor.query.get(id)
            actor.delete()

            return jsonify({
                'success': True,
                'deleted_id': actor.id
            })
        except:
            abort(422)

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

        if not movie:
            abort(404)

        return jsonify({
            'success': True,
            'movie': movie.format()
        })

    @app.route('/movies/', methods=['POST'])
    def create_movie():
        form = request.get_json()

        if not form.get('title') or not form.get('release_date'):
            abort(400)

        release_date = datetime.strptime(form.get('release_date'), '%Y-%m-%d')

        movie = Movie(form.get('title'), release_date)

        if (form.get('actors')):
            for actor_id in form.get('actors'):
                actor = Actor.query.get(actor_id)
                if actor:
                    movie.movies.append(actor)

        movie.insert()
        # TODO: Check if inserted
        return jsonify({
            'success': True,
            'movie': movie.format()
        }), 201

    @app.route('/movies/<int:id>', methods=['PATCH'])
    def update_movie(id):
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
                'movie': movie.format()
            })
        except:
            abort(422)

    @app.route('/movies/<int:id>', methods=['DELETE'])
    def delete_movie(id):
        try:
            movie = Movie.query.get(id)
            movie.delete()

            return jsonify({
                'success': True,
                'deleted_id': movie.id
            })
        except:
            abort(422)

    # Add/remove actors to/from movies

    @app.route('/movies/<int:movie_id>/<int:actor_id>', methods=['POST'])
    def add_actor_to_movie(movie_id, actor_id):
        movie = Movie.query.get(movie_id)
        actor = Actor.query.get(actor_id)

        movie.actors.append(actor)
        movie.update()

        return jsonify({
            'success': True,
            'movie': movie.format()
        })

    @app.route('/movies/<int:movie_id>/<int:actor_id>', methods=['DELETE'])
    def remove_actor_from_movie(movie_id, actor_id):
        movie = Movie.query.get(movie_id)
        actor = Actor.query.get(actor_id)

        movie.actors.remove(actor)
        movie.update()

        return jsonify({
            'success': True,
            'movie': movie.format()
        })

    # Add/remove movies to/from actors
    @app.route('/actors/<int:actor_id>/<int:movie_id>', methods=['POST'])
    def add_movie_to_actor(movie_id, actor_id):
        movie = Movie.query.get(movie_id)
        actor = Actor.query.get(actor_id)

        actor.movies.append(movie)
        actor.update()

        return jsonify({
            'success': True,
            'actor': actor.format()
        })

    @app.route('/actors/<int:actor_id>/<int:movie_id>', methods=['DELETE'])
    def remove_movie_from_actors(movie_id, actor_id):
        movie = Movie.query.get(movie_id)
        actor = Actor.query.get(actor_id)

        actor.movies.remove(movie)
        actor.update()

        return jsonify({
            'success': True,
            'actor': actor.format()
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

    return app
