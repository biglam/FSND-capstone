import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db


def generateAuthHeaders(jwt):
    return {
        'Authorization': 'Bearer ' + jwt
    }


casting_assistant_jwt = os.environ.get('CASTING_ASSISTANT_JWT')
casting_director_jwt = os.environ.get('CASTING_DIRECTOR_JWT')
exec_producer_jwt = os.environ.get('EXECUTIVE_DIRECTOR_JWT')


class MovieActorsTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ.get('DATABASE_URL')

        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass

    # Happy path tests
    ## Movies
    def test_get_movies(self):
        response = self.client().get('/movies', headers=generateAuthHeaders(casting_assistant_jwt))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['movies']), 4)
        self.assertTrue(data['movies'][0]['title'])
        self.assertTrue(data['movies'][0]['release_date'])

    def test_get_movie(self):
        response = self.client().get('/movies/1', headers=generateAuthHeaders(casting_assistant_jwt))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['title'], 'movie 1')
        self.assertEqual(data['movie']['release_date'], 'Tue, 01 Feb 2000 00:00:00 GMT')

    def test_create_movie(self):
        form = {
            'title': 'foobar the movie',
            'release_date': '2020-12-31'
        }

        response = self.client().post('/movies/', json=form, headers=generateAuthHeaders(exec_producer_jwt))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['id'], 5)
        self.assertEqual(data['movie']['title'], 'foobar the movie')
        self.assertEqual(data['movie']['release_date'], 'Thu, 31 Dec 2020 00:00:00 GMT')

    def test_update_movie(self):
        form = {
            'title': 'baz the movie',
            'release_date': '2021-11-21'
        }

        response = self.client().patch('/movies/1', json=form, headers=generateAuthHeaders(exec_producer_jwt))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['id'], 1)
        self.assertEqual(data['movie']['title'], 'baz the movie')
        self.assertEqual(data['movie']['release_date'], 'Sun, 21 Nov 2021 00:00:00 GMT')

    def test_delete_movie(self):
        response = self.client().delete('/movies/5', headers=generateAuthHeaders(exec_producer_jwt))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_id'], 5)

    def test_add_actor_to_movie(self):
        response = self.client().put('/movies/2/actors/3', headers=generateAuthHeaders(exec_producer_jwt))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['actors'][3]['id'], 3)

    def test_remove_actor_from_movie(self):
        response = self.client().delete('/movies/3/actors/1', headers=generateAuthHeaders(exec_producer_jwt))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['movie']['actors']), 0)

    ## Actors
    def test_get_actors(self):
        response = self.client().get('/actors', headers=generateAuthHeaders(casting_assistant_jwt))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['actors']), 4)
        self.assertTrue(data['actors'][0]['name'])
        self.assertTrue(data['actors'][0]['gender'])
        self.assertTrue(data['actors'][0]['age'])

    def test_get_actor(self):
        response = self.client().get('/actors/1', headers=generateAuthHeaders(casting_assistant_jwt))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['name'], 'jim')
        self.assertEqual(data['actor']['age'], 50)
        self.assertEqual(data['actor']['gender'], 'male')

    def test_create_actor(self):
        form = {
            'name': 'jill',
            'age': 21,
            'gender': 'female'
        }

        response = self.client().post('/actors/', json=form, headers=generateAuthHeaders(casting_director_jwt))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['id'], 5)
        self.assertEqual(data['actor']['name'], 'jill')
        self.assertEqual(data['actor']['age'], 21)
        self.assertEqual(data['actor']['gender'], 'female')

    #
    def test_update_actor(self):
        form = {
            'name': 'jimmy',
            'age': 25,
            'gender': 'male'
        }

        response = self.client().patch('/actors/2', json=form, headers=generateAuthHeaders(casting_director_jwt))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['id'], 2)
        self.assertEqual(data['actor']['name'], 'jimmy')
        self.assertEqual(data['actor']['age'], 25)
        self.assertEqual(data['actor']['gender'], 'male')

    def test_delete_actor(self):
        response = self.client().delete('/actors/5', headers=generateAuthHeaders(casting_director_jwt))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_id'], 5)

    def test_add_movie_to_actor(self):
        response = self.client().put('/actors/2/movies/4', headers=generateAuthHeaders(casting_director_jwt))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['movies'][2]['id'], 4)

    def test_remove_movie_from_actor(self):
        response = self.client().delete('/actors/4/movies/4', headers=generateAuthHeaders(casting_director_jwt))

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['actor']['movies']), 2)

    # Authorisation
    def test_create_movie_when_casting_assistant(self):
        form = {
            'title': 'foobar the movie',
            'release_date': '2020-12-31'
        }

        response = self.client().post('/movies/', json=form, headers=generateAuthHeaders(casting_assistant_jwt))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['code'], 'unauthorised')
        self.assertEqual(data['message']['description'], 'unauthorised for this resource')

    def test_create_movie_when_casting_director(self):
        form = {
            'title': 'foobar the movie',
            'release_date': '2020-12-31'
        }

        response = self.client().post('/movies/', json=form, headers=generateAuthHeaders(casting_director_jwt))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['code'], 'unauthorised')
        self.assertEqual(data['message']['description'], 'unauthorised for this resource')

    def test_update_movie_when_casting_assistant(self):
        form = {
            'title': 'baz the movie',
            'release_date': '2021-11-21'
        }

        response = self.client().patch('/movies/1', json=form, headers=generateAuthHeaders(casting_assistant_jwt))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['code'], 'unauthorised')
        self.assertEqual(data['message']['description'], 'unauthorised for this resource')

    def test_delete_movie_when_casting_assistant(self):
        response = self.client().delete('/movies/5', headers=generateAuthHeaders(casting_assistant_jwt))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['code'], 'unauthorised')
        self.assertEqual(data['message']['description'], 'unauthorised for this resource')

    def test_delete_movie_when_casting_director(self):
        response = self.client().delete('/movies/5', headers=generateAuthHeaders(casting_director_jwt))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['code'], 'unauthorised')
        self.assertEqual(data['message']['description'], 'unauthorised for this resource')

    def test_create_actor_when_casting_assistant(self):
        form = {
            'name': 'jill',
            'age': 21,
            'gender': 'female'
        }

        response = self.client().post('/actors/', json=form, headers=generateAuthHeaders(casting_assistant_jwt))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['code'], 'unauthorised')
        self.assertEqual(data['message']['description'], 'unauthorised for this resource')

    def test_update_actor_when_casting_assistant(self):
        form = {
            'name': 'jimmy',
            'age': 25,
            'gender': 'male'
        }

        response = self.client().patch('/actors/2', json=form,
                                       headers=generateAuthHeaders(casting_assistant_jwt))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['code'], 'unauthorised')
        self.assertEqual(data['message']['description'], 'unauthorised for this resource')

    def test_delete_actor_when_casting_assistant(self):
        response = self.client().delete('/actors/5', headers=generateAuthHeaders(casting_assistant_jwt))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['code'], 'unauthorised')
        self.assertEqual(data['message']['description'], 'unauthorised for this resource')

    # Error handling
    def test_page_not_found(self):
        response = self.client().get('/fakepage', headers=generateAuthHeaders(exec_producer_jwt))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'page not found')

    def test_get_actor_not_found(self):
        response = self.client().get('/actors/1000', headers=generateAuthHeaders(exec_producer_jwt))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'page not found')

    def test_create_actor_empty_form(self):
        response = self.client().post('/actors/', json={}, headers=generateAuthHeaders(exec_producer_jwt))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_update_actor_not_found(self):
        response = self.client().patch('/actors/1000', json={'name': 'bob'},
                                       headers=generateAuthHeaders(exec_producer_jwt))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'page not found')

    def test_update_actor_empty_form(self):
        response = self.client().patch('/actors/1', json={}, headers=generateAuthHeaders(exec_producer_jwt))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_delete_actor_not_found(self):
        response = self.client().delete('/actors/1000', headers=generateAuthHeaders(exec_producer_jwt))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_get_movie_not_found(self):
        response = self.client().get('/movies/1000', headers=generateAuthHeaders(exec_producer_jwt))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'page not found')

    def test_create_movie_empty_form(self):
        response = self.client().post('/movies/', json={}, headers=generateAuthHeaders(exec_producer_jwt))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_create_movie_no_title(self):
        response = self.client().post('/movies/', json={'release_date': '2000-01-01'},
                                      headers=generateAuthHeaders(exec_producer_jwt))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_create_movie_no_release_date(self):
        response = self.client().post('/movies/', json={'title': 'jaws'},
                                      headers=generateAuthHeaders(exec_producer_jwt))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_update_movies_not_found(self):
        response = self.client().patch('/movies/1000', json={'title': 'jaws'},
                                       headers=generateAuthHeaders(exec_producer_jwt))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'page not found')

    def test_update_movies_empty_form(self):
        response = self.client().patch('/movies/1', json={}, headers=generateAuthHeaders(exec_producer_jwt))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_delete_movie_not_found(self):
        response = self.client().delete('/movies/1000', headers=generateAuthHeaders(exec_producer_jwt))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
    # Make the tests conveniently executable


if __name__ == "__main__":
    unittest.main()
