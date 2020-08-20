import os
from flask import Flask, request, abort, jsonify
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import models
import json
from auth import AuthError, check_auth


def cprint(label, data):
    print("")
    print(label)
    print(data)
    print("")


def json_formatter(model, data):
    json_formatted = []

    if model == "Movies":
        for x in data:
            new_dict = {
                "id": str(
                    x.id), "title": x.title, "release_date": str(
                    x.release_date)}
            json_formatted.append(new_dict)
    elif model == "Actor":
        for x in data:
            new_dict = {
                "id": str(
                    x.id), "name": x.name, "age": str(
                    x.age), "gender": x.gender}
            json_formatted.append(new_dict)

    return json.dumps(json_formatted)


def create_app(test_config=None):

    app = Flask(__name__)
    # models.db_drop_and_create_all()
    models.setup_db(app)
    CORS(app)

    # ++++++++++++++++++++++ HOME ROUTE ++++++++++++++++++++++
    @app.route('/')
    def home_test_route():
        return "This is your home test route for your capstone project"

    @app.route('/headers', methods=["GET"])
    def headers(token):
        return 'token'


# =========================================================================
# 								ACTOR ROUTES
# =========================================================================

    # ++++++++++++++++++++++ GET ACTORS ++++++++++++++++++++++

    @app.route('/actors', methods=['GET'])
    @check_auth('get:actors')
    def get_actors(payload):
        all_actors = models.Actor.query.all()
        formatted_response = json_formatter("Actor", all_actors)
        return formatted_response

    # ++++++++++++++++++++++ POST New ACTORS ++++++++++++++++++++++
    @app.route('/actors', methods=['POST'])
    @check_auth('post:actors')
    def post_new_actors(payload):
        req_data = json.loads(request.data.decode("utf-8"))
        try:
            model_format = models.Actor(
                name=req_data["name"],
                age=req_data["age"],
                gender=req_data["gender"])
            models.Actor.insert(model_format)
        except Exception as e:
            print(e)
            print("New actor failed to post to database.")
        return json.dumps(req_data), 200

    # ++++++++++++++++++++++ PATCH ACTOR ++++++++++++++++++++++
    @app.route('/actor/<int:actor_id>', methods=['GET', 'PATCH'])
    @check_auth('patch:actors')
    def patch_actor(actor_id, payload):
        req_data = json.loads(request.data.decode("utf-8"))
        actor = [models.Actor.query.filter(
            models.Actor.id == actor_id).one_or_none()]
        actor[0].name = req_data["name"]
        actor[0].age = req_data["age"]
        actor[0].gender = req_data["gender"]
        formatted_response = json_formatter("Actor", actor)
        actor[0].update()
        return formatted_response, 200

    # ++++++++++++++++++++++ DELETE ACTOR ++++++++++++++++++++++
    @app.route('/actor/<int:actor_id>/delete', methods=['DELETE'])
    @check_auth('delete:actors')
    def delete_actor(actor_id, payload):
        actor = models.Actor.query.filter(
            models.Actor.id == actor_id).one_or_none()
        name = actor.name
        actor.delete()
        return name + " has been removed from the database.", 200


# =========================================================================
# 								MOVIE ROUTES
# =========================================================================

    # ++++++++++++++++++++++ GET MOVIES ++++++++++++++++++++++


    @app.route('/movies', methods=['GET'])
    @check_auth('get:movies')
    def get_movies(payload):
        all_movies = models.Movies.query.all()
        formatted_response = json_formatter("Movies", all_movies)
        return formatted_response

    # ++++++++++++++++++++++ POST New Movie ++++++++++++++++++++++
    @app.route('/movies', methods=['POST'])
    @check_auth('post:movies')
    def post_new_movie(payload):
        req_data = json.loads(request.data.decode("utf-8"))
        date = req_data["release_date"]
        if isinstance(date, str):
            date = datetime.strptime(
                req_data["release_date"],
                '%Y-%m-%d %H:%M:%S.%f')
        try:
            model_format = models.Movies(
                title=req_data["title"], release_date=date)
            models.Movies.insert(model_format)
        except Exception as e:
            print(e)
            print("New movie failed to post to database.")
        return json.dumps(req_data), 200

    # ++++++++++++++++++++++ PATCH MOVIE ++++++++++++++++++++++

    @app.route('/movies/<int:movie_id>', methods=['GET', 'PATCH'])
    @check_auth('patch:movies')
    def patch_movie(movie_id, payload):
        req_data = json.loads(request.data.decode("utf-8"))
        movie = [models.Movies.query.filter(
            models.Movies.id == movie_id).one_or_none()]
        movie[0].title = req_data["title"]
        movie[0].release_date = datetime.strptime(
            req_data["release_date"], '%Y-%m-%d %H:%M:%S.%f')
        formatted_response = json_formatter("Movies", movie)
        movie[0].update()
        return formatted_response, 200

    # ++++++++++++++++++++++ DELETE Movie ++++++++++++++++++++++
    @app.route('/movie/<int:movie_id>/delete', methods=['DELETE'])
    @check_auth('delete:movies')
    def delete_movie(movie_id, payload):
        movie = models.Movies.query.filter(models.Movies.id == movie_id).one_or_none()
        title = movie.title
        movie.delete()
        return title + " has been removed from the database.", 200

# =========================================================================
# 								ERROR HANDLING
# =========================================================================

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found."
        }), 404

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized."
        }), 401

    @app.errorhandler(403)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "Forbidden.  You do not have permissions to perform this action."
        }), 401


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
