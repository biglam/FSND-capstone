import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db

def generateAuthHeaders(jwt):
    return {
        'Authorization': 'Bearer ' + jwt
    }

class MovieActorsTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        postgres_username = os.environ.get('POSTGRES_USERNAME')
        postgres_password = os.environ.get('POSTGRES_PASSWORD')
        self.database_path = "postgres://{}:{}@{}/{}".format(postgres_username, postgres_password, 'localhost:5432', self.database_name)
        self.casting_assistant_jwt = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkIwbF9YZWlEVVlGTVdhbTZ2dS1YOSJ9.eyJpc3MiOiJodHRwczovL3VkYWMtY2Fwc3RvbmUuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmODA4NTk5NGU3MDM4MDA2ZjAwNDJiZiIsImF1ZCI6ImZzbmQtYXV0aCIsImlhdCI6MTYwMjI1ODM4MCwiZXhwIjoxNjAyMzQ0NzgwLCJhenAiOiI5UEJkR2h0bE9mUGVTVkFaUXhGVFdUaWxzM1JnYldkYiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.zexjHmt4OIQddgF3n0fOlWG3MuTlTBQMYfq6a_nkJYw5wyrapi3vvMRNKTMM9HQeNXmel5lUW0BJLjIt2b0abWX8uK2AD7bb2_bW-UOSKXX9dy_oe9oAtlfegRZdAFJsEUQeKFlXT4GblUiuRdHdQGPkN_l-Fx12ldvSr3I8GYVhLivi2TMdNIVO_M7RnJ1Pljl7_3ra8jYgPPXrIGepIBxe1FV9AaC4UvULs1gR1Di72XQ6bFn-kzFLJLmAlU6-0cx2StegRl0GBUqFPV_f_QLDzELn_QWLo_zDXfwjmTCLaGBdA3OajooFN03tyVvMa4ku5iBsU6KjDebecNLFgg"
        self.casting_director_jwt = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkIwbF9YZWlEVVlGTVdhbTZ2dS1YOSJ9.eyJpc3MiOiJodHRwczovL3VkYWMtY2Fwc3RvbmUuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmODBhYWE0OGQyNWEyMDA3NWMyOTBhYSIsImF1ZCI6ImZzbmQtYXV0aCIsImlhdCI6MTYwMjI2Nzg4NiwiZXhwIjoxNjAyMzU0Mjg2LCJhenAiOiI5UEJkR2h0bE9mUGVTVkFaUXhGVFdUaWxzM1JnYldkYiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.sjHKoE_11dTBWdCDdl35TcRxwcQTz2V0kmdalMuUF6UjyY9niPqj6qSwV3zNv_w5g3937KY13OQwTo9BNkF1twi0VS2pDC8M9QNhzIlFWQVud9TUQIlfZHUBD0WDxWuMPahotcXTZn8RPp6oC60RRAa3PFeu_1xLHtXfoKKi-qOFXkTsIKaSUSQ4O0-JzMZAUZHN4x0haz29bTZqT__b2jurb_3zY_kGPBm3_nx-NjxmH2rDX8xEG0KcUelv3s_CbY5SF97rUVTx9ZZMptqbn-p7EHeWZ2v_IjwN8fFGpAYWVQoKKVelM39dVGcUTFwMGFXxMCUqsGTwVNrtmglqqg"
        self.exec_producer_jwt = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkIwbF9YZWlEVVlGTVdhbTZ2dS1YOSJ9.eyJpc3MiOiJodHRwczovL3VkYWMtY2Fwc3RvbmUuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmODBhYzE0MWU5NDViMDA2OWJlOWIwYiIsImF1ZCI6ImZzbmQtYXV0aCIsImlhdCI6MTYwMjI2ODIxOSwiZXhwIjoxNjAyMzU0NjE5LCJhenAiOiI5UEJkR2h0bE9mUGVTVkFaUXhGVFdUaWxzM1JnYldkYiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.UPM4yXQeiQuR0iYNu8tu9xEfnDfVDAlmZ_O-aHhRHvXHzdeRM5_U-2s-ecHc5N-Y6i3fW99jG2ob7v7hJirHkyo88-iW9f3_yJ0Y2QByTzRYVIQqsDEjw_fKbF3LRHA--j8Ia3wDLo0GQeQAnFj7Pwc-QxZpU9uj4xmzNCwFXbm2Lqzywmff9XqoM1MQjp22QG6BSFhXqQjr8edhG-eqi7dCfCplCo2kAIaFcgBdfcjr6svAZkjsC6pfuta1Hj8TFwtd-f3lvm3fNKJ9ox1O9qUR1rX7vwYaTW8FJG1MSoedUnHdUUBLDdRwUZx6bVwvzp_DzpiV6j9Wsf0LBz54Vg"

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
        response = self.client().get('/movies', headers=generateAuthHeaders(self.casting_assistant_jwt))
        data = json.loads(response.data)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(data['success'], True)
        self.assertEquals(len(data['movies']), 4)
        self.assertTrue(data['movies'][0]['title'])
        self.assertTrue(data['movies'][0]['release_date'])

    def test_get_movie(self):
        response = self.client().get('/movies/1', headers=generateAuthHeaders(self.casting_assistant_jwt))
        data = json.loads(response.data)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(data['success'], True)
        self.assertEquals(data['movie']['title'], 'movie 1')
        self.assertTrue(data['movie']['release_date']) # TODO: assert date

    def test_create_movie(self):
        form = {
            'title': 'foobar the movie',
            'release_date': '2020-12-31'
        }

        response = self.client().post('/movies/', json=form, headers=generateAuthHeaders(self.exec_producer_jwt))
        data = json.loads(response.data)
        self.assertEquals(response.status_code, 201)
        self.assertEquals(data['success'], True)
        self.assertEquals(data['movie']['id'], 5)
        self.assertEquals(data['movie']['title'], 'foobar the movie')
        self.assertEquals(data['movie']['release_date'], 'Thu, 31 Dec 2020 00:00:00 GMT')

    def test_update_movie(self):
        form = {
            'title': 'baz the movie',
            'release_date': '2021-11-21'
        }

        response = self.client().patch('/movies/1', json=form, headers=generateAuthHeaders(self.exec_producer_jwt))
        data = json.loads(response.data)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(data['success'], True)
        self.assertEquals(data['movie']['id'], 1)
        self.assertEquals(data['movie']['title'], 'baz the movie')
        self.assertEquals(data['movie']['release_date'], 'Sun, 21 Nov 2021 00:00:00 GMT')

    def test_delete_movie(self):
        response = self.client().delete('/movies/5', headers=generateAuthHeaders(self.exec_producer_jwt))
        data = json.loads(response.data)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(data['success'], True)
        self.assertEquals(data['deleted_id'], 5)

    def test_add_actor_to_movie(self):
        response = self.client().put('/movies/2/actors/3', headers=generateAuthHeaders(self.exec_producer_jwt))
        data = json.loads(response.data)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(data['success'], True)
        self.assertEquals(data['movie']['actors'][3]['id'], 3)

    def test_remove_actor_from_movie(self):
        response = self.client().delete('/movies/3/actors/1', headers=generateAuthHeaders(self.exec_producer_jwt))
        data = json.loads(response.data)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(data['success'], True)
        self.assertEquals(len(data['movie']['actors']), 0)

    ## Actors
    def test_get_actors(self):
        response = self.client().get('/actors', headers=generateAuthHeaders(self.casting_assistant_jwt))
        data = json.loads(response.data)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(data['success'], True)
        self.assertEquals(len(data['actors']), 4)
        self.assertTrue(data['actors'][0]['name'])
        self.assertTrue(data['actors'][0]['gender'])
        self.assertTrue(data['actors'][0]['age'])

    def test_get_actor(self):
        response = self.client().get('/actors/1', headers=generateAuthHeaders(self.casting_assistant_jwt))
        data = json.loads(response.data)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(data['success'], True)
        self.assertEquals(data['actor']['name'], 'jim')
        self.assertEquals(data['actor']['age'], 50)
        self.assertEquals(data['actor']['gender'], 'male')


    def test_create_actor(self):
        form = {
            'name': 'jill',
            'age': 21,
            'gender': 'female'
        }

        response = self.client().post('/actors/', json=form, headers=generateAuthHeaders(self.casting_director_jwt))
        data = json.loads(response.data)
        self.assertEquals(response.status_code, 201)
        self.assertEquals(data['success'], True)
        self.assertEquals(data['actor']['id'], 5)
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

        response = self.client().patch('/actors/2', json=form, headers=generateAuthHeaders(self.casting_director_jwt))
        data = json.loads(response.data)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(data['success'], True)
        self.assertEquals(data['actor']['id'], 2)
        self.assertEquals(data['actor']['name'], 'jimmy')
        self.assertEquals(data['actor']['age'], 25)
        self.assertEquals(data['actor']['gender'], 'male')

    def test_delete_actor(self):
        response = self.client().delete('/actors/5', headers=generateAuthHeaders(self.casting_director_jwt))
        data = json.loads(response.data)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(data['success'], True)
        self.assertEquals(data['deleted_id'], 5)

    def test_add_movie_to_actor(self):
        response = self.client().put('/actors/2/movies/4', headers=generateAuthHeaders(self.casting_director_jwt))
        data = json.loads(response.data)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(data['success'], True)
        self.assertEquals(data['actor']['movies'][2]['id'], 4)

    def test_remove_movie_from_actor(self):
        response = self.client().delete('/actors/4/movies/4', headers=generateAuthHeaders(self.casting_director_jwt))

        data = json.loads(response.data)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(data['success'], True)
        self.assertEquals(len(data['actor']['movies']), 2)

    # Authorisation
    def test_create_movie_when_casting_assistant(self):
        form = {
            'title': 'foobar the movie',
            'release_date': '2020-12-31'
        }

        response = self.client().post('/movies/', json=form, headers=generateAuthHeaders(self.casting_assistant_jwt))
        data = json.loads(response.data)
        self.assertEquals(response.status_code, 403)
        self.assertEquals(data['success'], False)
        self.assertEquals(data['message']['code'], 'unauthorised')
        self.assertEquals(data['message']['description'], 'unauthorised for this resource')

    def test_create_movie_when_casting_director(self):
        form = {
            'title': 'foobar the movie',
            'release_date': '2020-12-31'
        }

        response = self.client().post('/movies/', json=form, headers=generateAuthHeaders(self.casting_director_jwt))
        data = json.loads(response.data)
        self.assertEquals(response.status_code, 403)
        self.assertEquals(data['success'], False)
        self.assertEquals(data['message']['code'], 'unauthorised')
        self.assertEquals(data['message']['description'], 'unauthorised for this resource')


    def test_update_movie_when_casting_assistant(self):
        form = {
            'title': 'baz the movie',
            'release_date': '2021-11-21'
        }

        response = self.client().patch('/movies/1', json=form, headers=generateAuthHeaders(self.casting_assistant_jwt))
        data = json.loads(response.data)
        self.assertEquals(response.status_code, 403)
        self.assertEquals(data['success'], False)
        self.assertEquals(data['message']['code'], 'unauthorised')
        self.assertEquals(data['message']['description'], 'unauthorised for this resource')

    def test_delete_movie_when_casting_assistant(self):
        response = self.client().delete('/movies/5', headers=generateAuthHeaders(self.casting_assistant_jwt))
        data = json.loads(response.data)

        self.assertEquals(response.status_code, 403)
        self.assertEquals(data['success'], False)
        self.assertEquals(data['message']['code'], 'unauthorised')
        self.assertEquals(data['message']['description'], 'unauthorised for this resource')

    def test_delete_movie_when_casting_director(self):
        response = self.client().delete('/movies/5', headers=generateAuthHeaders(self.casting_director_jwt))
        data = json.loads(response.data)

        self.assertEquals(response.status_code, 403)
        self.assertEquals(data['success'], False)
        self.assertEquals(data['message']['code'], 'unauthorised')
        self.assertEquals(data['message']['description'], 'unauthorised for this resource')

    def test_create_actor_when_casting_assistant(self):
        form = {
            'name': 'jill',
            'age': 21,
            'gender': 'female'
        }

        response = self.client().post('/actors/', json=form, headers=generateAuthHeaders(self.casting_assistant_jwt))
        data = json.loads(response.data)
        self.assertEquals(response.status_code, 403)
        self.assertEquals(data['success'], False)
        self.assertEquals(data['message']['code'], 'unauthorised')
        self.assertEquals(data['message']['description'], 'unauthorised for this resource')


    def test_update_actor_when_casting_assistant(self):
        form = {
            'name': 'jimmy',
            'age': 25,
            'gender': 'male'
        }

        response = self.client().patch('/actors/2', json=form,
                                       headers=generateAuthHeaders(self.casting_assistant_jwt))
        data = json.loads(response.data)
        self.assertEquals(response.status_code, 403)
        self.assertEquals(data['success'], False)
        self.assertEquals(data['message']['code'], 'unauthorised')
        self.assertEquals(data['message']['description'], 'unauthorised for this resource')

    def test_delete_actor_when_casting_assistant(self):
        response = self.client().delete('/actors/5', headers=generateAuthHeaders(self.casting_assistant_jwt))
        data = json.loads(response.data)

        self.assertEquals(response.status_code, 403)
        self.assertEquals(data['success'], False)
        self.assertEquals(data['message']['code'], 'unauthorised')
        self.assertEquals(data['message']['description'], 'unauthorised for this resource')

    # Error handling
    def test_page_not_found(self):
        response = self.client().get('/fakepage', headers=generateAuthHeaders(self.exec_producer_jwt))
        data = json.loads(response.data)

        self.assertEquals(response.status_code, 404)
        self.assertEquals(data['success'], False)
        self.assertEquals(data['message'], 'page not found')

    def test_get_actor_not_found(self):
        response = self.client().get('/actors/1000', headers=generateAuthHeaders(self.exec_producer_jwt))
        data = json.loads(response.data)

        self.assertEquals(response.status_code, 404)
        self.assertEquals(data['success'], False)
        self.assertEquals(data['message'], 'page not found')

    def test_create_actor_empty_form(self):
        response = self.client().post('/actors/', json={}, headers=generateAuthHeaders(self.exec_producer_jwt))
        data = json.loads(response.data)

        self.assertEquals(response.status_code, 400)
        self.assertEquals(data['success'], False)
        self.assertEquals(data['message'], 'bad request')

    def test_update_actor_not_found(self):
        response = self.client().patch('/actors/1000', json={ 'name': 'bob' }, headers=generateAuthHeaders(self.exec_producer_jwt))
        data = json.loads(response.data)

        self.assertEquals(response.status_code, 404)
        self.assertEquals(data['success'], False)
        self.assertEquals(data['message'], 'page not found')

    def test_update_actor_empty_form(self):
        response = self.client().patch('/actors/1', json={}, headers=generateAuthHeaders(self.exec_producer_jwt))
        data = json.loads(response.data)

        self.assertEquals(response.status_code, 400)
        self.assertEquals(data['success'], False)
        self.assertEquals(data['message'], 'bad request')

    def test_delete_actor_not_found(self):
        response = self.client().delete('/actors/1000', headers=generateAuthHeaders(self.exec_producer_jwt))
        data = json.loads(response.data)

        self.assertEquals(response.status_code, 422)
        self.assertEquals(data['success'], False)
        self.assertEquals(data['message'], 'unprocessable')


    def test_get_movie_not_found(self):
        response = self.client().get('/movies/1000', headers=generateAuthHeaders(self.exec_producer_jwt))
        data = json.loads(response.data)

        self.assertEquals(response.status_code, 404)
        self.assertEquals(data['success'], False)
        self.assertEquals(data['message'], 'page not found')

    def test_create_movie_empty_form(self):
        response = self.client().post('/movies/', json={}, headers=generateAuthHeaders(self.exec_producer_jwt))
        data = json.loads(response.data)

        self.assertEquals(response.status_code, 400)
        self.assertEquals(data['success'], False)
        self.assertEquals(data['message'], 'bad request')

    def test_create_movie_no_title(self):
        response = self.client().post('/movies/', json={ 'release_date': '2000-01-01'}, headers=generateAuthHeaders(self.exec_producer_jwt))
        data = json.loads(response.data)

        self.assertEquals(response.status_code, 400)
        self.assertEquals(data['success'], False)
        self.assertEquals(data['message'], 'bad request')

    def test_create_movie_no_release_date(self):
        response = self.client().post('/movies/', json={ 'title': 'jaws' }, headers=generateAuthHeaders(self.exec_producer_jwt))
        data = json.loads(response.data)

        self.assertEquals(response.status_code, 400)
        self.assertEquals(data['success'], False)
        self.assertEquals(data['message'], 'bad request')

    def test_update_movies_not_found(self):
        response = self.client().patch('/movies/1000', json={ 'title': 'jaws' }, headers=generateAuthHeaders(self.exec_producer_jwt))
        data = json.loads(response.data)

        self.assertEquals(response.status_code, 404)
        self.assertEquals(data['success'], False)
        self.assertEquals(data['message'], 'page not found')

    def test_update_movies_empty_form(self):
        response = self.client().patch('/movies/1', json={}, headers=generateAuthHeaders(self.exec_producer_jwt))
        data = json.loads(response.data)

        self.assertEquals(response.status_code, 400)
        self.assertEquals(data['success'], False)
        self.assertEquals(data['message'], 'bad request')

    def test_delete_movie_not_found(self):
        response = self.client().delete('/movies/1000', headers=generateAuthHeaders(self.exec_producer_jwt))
        data = json.loads(response.data)

        self.assertEquals(response.status_code, 422)
        self.assertEquals(data['success'], False)
        self.assertEquals(data['message'], 'unprocessable')
    # Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()