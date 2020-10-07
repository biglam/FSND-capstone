import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import date

from flaskr import create_app
from models import setup_db, Actor, Movie

class MovieActorsTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        postgres_username = os.environ.get('POSTGRES_USERNAME')
        postgres_password = os.environ.get('POSTGRES_PASSWORD')
        self.database_path = "postgres://{}:{}@{}/{}".format(postgres_username, postgres_password, 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # Happy path tests
    ## Movies
    def test_get_movies(self):
        response = self.client().get('/movies')
        data = json.loads(response.data)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(data['success'], True)
        self.assertEquals(len(data['movies']), 3)
        self.assertTrue(data['movies'][0]['title'])
        self.assertTrue(data['movies'][0]['release_date'])

    def test_get_movie(self):
        response = self.client().get('/movies/1')
        data = json.loads(response.data)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(data['success'], True)
        self.assertEquals(data['movie']['title'], 'Foobar')
        self.assertTrue(data['movie']['release_date']) # TODO: assert date

    def test_create_movie(self):
        form = {
            'title': 'foobar the movie',
            'release_date': '2020-12-31'
        }

        response = self.client().post('/movies/', json=form)
        data = json.loads(response.data)
        self.assertEquals(response.status_code, 201)
        self.assertEquals(data['success'], True)
        self.assertEquals(data['movie']['id'], 7)
        self.assertEquals(data['movie']['title'], 'foobar the movie')
        self.assertEquals(data['movie']['release_date'], 'Thu, 31 Dec 2020 00:00:00 GMT')

    def test_update_movie(self):
        form = {
            'title': 'baz the movie',
            'release_date': '2021-11-21'
        }

        response = self.client().patch('/movies/1', json=form)
        data = json.loads(response.data)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(data['success'], True)
        self.assertEquals(data['movie']['id'], 1)
        self.assertEquals(data['movie']['title'], 'baz the movie')
        self.assertEquals(data['movie']['release_date'], 'Sun, 21 Nov 2021 00:00:00 GMT')

    def test_delete_movie(self):
        response = self.client().delete('/movies/7')
        data = json.loads(response.data)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(data['success'], True)
        self.assertEquals(data['deleted_id'], 7)

    ## Actors
    def test_get_actors(self):
        response = self.client().get('/actors')
        data = json.loads(response.data)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(data['success'], True)
        self.assertEquals(len(data['actors']), 2)
        self.assertTrue(data['actors'][0]['name'])
        self.assertTrue(data['actors'][0]['gender'])
        self.assertTrue(data['actors'][0]['age'])

    def test_get_actor(self):
        response = self.client().get('/actors/2')
        data = json.loads(response.data)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(data['success'], True)
        self.assertEquals(data['actor']['name'], 'billy')
        self.assertEquals(data['actor']['age'], 50)
        self.assertEquals(data['actor']['gender'], 'male')

    def test_create_actor(self):
        form = {
            'name': 'jill',
            'age': 21,
            'gender': 'female'
        }

        response = self.client().post('/actors/', json=form)
        data = json.loads(response.data)
        self.assertEquals(response.status_code, 201)
        self.assertEquals(data['success'], True)
        self.assertEquals(data['actor']['id'], 4)
        self.assertEquals(data['actor']['name'], 'jill')
        self.assertEquals(data['actor']['age'], 21)
        self.assertEquals(data['actor']['gender'], 'female')
    #
    def test_update_actor(self):
        form = {
            'name': 'jimmy',
            'age': 25,
            'gender': 'male'
        }

        response = self.client().patch('/actors/2', json=form)
        data = json.loads(response.data)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(data['success'], True)
        self.assertEquals(data['actor']['id'], 2)
        self.assertEquals(data['actor']['name'], 'jimmy')
        self.assertEquals(data['actor']['age'], 25)
        self.assertEquals(data['actor']['gender'], 'male')

    def test_delete_actor(self):
        response = self.client().delete('/actors/4')
        data = json.loads(response.data)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(data['success'], True)
        self.assertEquals(data['deleted_id'], 4)

    # Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()