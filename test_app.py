import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app, json_formatter
from models import setup_db, Movies, Actor
from datetime import datetime
from config import tokens


def cprint(label, data):
    print("")
    print(label)
    print(data)
    print("")


assistant_token = {
    'Authorization': tokens['assistant_token']
}

director_token = {
    'Authorization': tokens['director_token']
}

producer_token = {
    'Authorization': tokens['producer_token']
}


class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ.get("DATABASE_URL")
        # self.database_path = "postgres://localhost:5432/casting_agency"

        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_actor = {"name": "This is a test actor",
                          "age": "55",
                          "gender": "Male"
                          }

        self.updated_actor = {"name": "This actor has been updated",
                              "age": "600",
                              "gender": "Female"
                              }
        self.reset_actor = {
            "id": "1",
            "name": "Charlize Theron",
            "age": "45",
            "gender": "Female"}

        self.new_movie = {
            "title": "This is a test movie from test_app.py",
            "release_date": "2021-08-17 21:14:47.095967"
        }
        self.updated_movie = {
            "title": "This movie has been updated",
            "release_date": "2021-08-17 21:14:47.095967"
        }
        self.reset_movie = {"title": "The Machinist: Updated",
                            "release_date": "2021-08-17 21:14:47.095967"
                            }

    def tearDown(self):
        """Executed after reach test"""
        pass

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #     ++++++++++++++++++++++++++++++  GET ALL ACTORS  +++++++++++++++++
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def test_get_actors_assistant(self):
        res = self.client().get("/actors", headers=assistant_token)
        data = json.loads(res.data)

        self.assertTrue(len(data) > 0)
        self.assertEqual(res.status_code, 200)

    def test_get_actors_director(self):
        res = self.client().get("/actors", headers=director_token)
        data = json.loads(res.data)

        self.assertTrue(len(data) > 0)
        self.assertEqual(res.status_code, 200)

    def test_get_actors_producer(self):
        res = self.client().get("/actors", headers=producer_token)
        data = json.loads(res.data)

        self.assertTrue(len(data) > 0)
        self.assertEqual(res.status_code, 200)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #     ++++++++++++++++++++++++++++++  POST NEW ACTOR  +++++++++++++++++
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def test_create_new_actor_assistant(self):
        res = self.client().post("/actors", json=self.new_actor, headers=assistant_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertTrue(res is not None)

    def test_create_new_actor_director(self):
        res = self.client().post("/actors", json=self.new_actor, headers=director_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(res is not None)

    def test_create_new_actor_producer(self):
        res = self.client().post("/actors", json=self.new_actor, headers=producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(res is not None)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #     ++++++++++++++++++++++++++++++  PATCH ACTOR  +++++++++++++++++
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def test_patch_actor_assistant(self):
        res = self.client().patch(
            "/actor/9",
            json=self.updated_actor,
            headers=assistant_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertTrue(res is not None)

    def test_patch_actor_director(self):
        res = self.client().patch(
            "/actor/9",
            json=self.updated_actor,
            headers=director_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(res is not None)

    def test_patch_actor_producer(self):
        res = self.client().patch(
            "/actor/9",
            json=self.updated_actor,
            headers=producer_token)
        cprint("test_patch_actor_producer res", res.data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(res is not None)

    def test_reset_actor(self):
        res = self.client().patch(
            "/actor/9",
            json=self.reset_actor,
            headers=producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(res is not None)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #     ++++++++++++++++++++++++++++++  DELETE ACTOR  +++++++++++++++++
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def test_delete_actors_assistant(self):
        all_actors = json.loads(json_formatter("Actor", Actor.query.all()))
        delete_actor_id = all_actors[len(all_actors) - 1]["id"]

        delete_endpoint = "/actor/" + str(delete_actor_id) + "/delete"
        res = self.client().delete(delete_endpoint, headers=assistant_token)
        data = res.data

        all_actors_len_check = len(
            json.loads(
                json_formatter(
                    "Actor",
                    Actor.query.all())))

        self.assertEqual(res.status_code, 403)

    def test_delete_actors_director(self):
        all_actors = json.loads(json_formatter("Actor", Actor.query.all()))
        delete_actor_id = all_actors[len(all_actors) - 1]["id"]

        delete_endpoint = "/actor/" + str(delete_actor_id) + "/delete"
        res = self.client().delete(delete_endpoint, headers=director_token)
        data = res.data

        all_actors_len_check = len(
            json.loads(
                json_formatter(
                    "Actor",
                    Actor.query.all())))

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(all_actors) - 1 == all_actors_len_check)

    def test_delete_actors_producer(self):
        all_actors = json.loads(json_formatter("Actor", Actor.query.all()))
        delete_actor_id = all_actors[len(all_actors) - 1]["id"]

        delete_endpoint = "/actor/" + str(delete_actor_id) + "/delete"
        res = self.client().delete(delete_endpoint, headers=producer_token)
        data = res.data

        all_actors_len_check = len(
            json.loads(
                json_formatter(
                    "Actor",
                    Actor.query.all())))

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(all_actors) - 1 == all_actors_len_check)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #     ++++++++++++++++++++++++++++++  GET ALL MOVIES  +++++++++++++++++
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def test_get_movies_assistant(self):
        res = self.client().get("/movies", headers=assistant_token)
        data = json.loads(res.data)

        self.assertTrue(len(data) > 0)
        self.assertEqual(res.status_code, 200)

    def test_get_movies_director(self):
        res = self.client().get("/movies", headers=director_token)
        data = json.loads(res.data)

        self.assertTrue(len(data) > 0)
        self.assertEqual(res.status_code, 200)

    def test_get_movies_producer(self):
        res = self.client().get("/movies", headers=producer_token)
        data = json.loads(res.data)

        self.assertTrue(len(data) > 0)
        self.assertEqual(res.status_code, 200)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #     ++++++++++++++++++++++++++++++  POST NEW MOVIE  +++++++++++++++++
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def test_create_new_movie_assistant(self):
        res = self.client().post("/movies", json=self.new_movie, headers=assistant_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertTrue(res is not None)

    def test_create_new_movie_director(self):
        res = self.client().post("/movies", json=self.new_movie, headers=director_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertTrue(res is not None)

    def test_create_new_movie_producer(self):
        res = self.client().post("/movies", json=self.new_movie, headers=producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(res is not None)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #     ++++++++++++++++++++++++++++++  PATCH MOVIE  +++++++++++++++++
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def test_patch_movie_assistant(self):
        res = self.client().patch(
            "/movies/1",
            json=self.updated_movie,
            headers=assistant_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertTrue(res is not None)

    def test_patch_movie_director(self):
        res = self.client().patch(
            "/movies/1",
            json=self.updated_movie,
            headers=director_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(res is not None)

    def test_patch_movie_producer(self):
        res = self.client().patch(
            "/movies/1",
            json=self.updated_movie,
            headers=producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(res is not None)

    def test_reset_movie(self):
        res = self.client().patch(
            "/movies/1",
            json=self.reset_movie,
            headers=producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(res is not None)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #     ++++++++++++++++++++++++++++++  DELETE MOVIE  +++++++++++++++++
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def test_delete_movie_assistant(self):
        all_movies = json.loads(json_formatter("Movies", Movies.query.all()))
        delete_movie_id = all_movies[len(all_movies) - 1]["id"]

        delete_endpoint = "/movie/" + str(delete_movie_id) + "/delete"
        res = self.client().delete(delete_endpoint, headers=assistant_token)
        data = res.data

        all_movies_len_check = json.loads(
            json_formatter("Movies", Movies.query.all()))

        self.assertEqual(res.status_code, 403)

    def test_delete_movie_director(self):
        all_movies = json.loads(json_formatter("Movies", Movies.query.all()))
        delete_movie_id = all_movies[len(all_movies) - 1]["id"]

        delete_endpoint = "/movie/" + str(delete_movie_id) + "/delete"
        res = self.client().delete(delete_endpoint, headers=director_token)
        data = res.data

        all_movies_len_check = json.loads(
            json_formatter("Movies", Movies.query.all()))

        self.assertEqual(res.status_code, 403)

    def test_delete_movie_producer(self):
        all_movies = json.loads(json_formatter("Movies", Movies.query.all()))
        delete_movie_id = all_movies[len(all_movies) - 1]["id"]

        delete_endpoint = "/movie/" + str(delete_movie_id) + "/delete"
        res = self.client().delete(delete_endpoint, headers=producer_token)
        data = res.data

        all_movies_len_check = json.loads(
            json_formatter("Movies", Movies.query.all()))

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(all_movies) - 1 == len(all_movies_len_check))


if __name__ == "__main__":
    unittest.main()
