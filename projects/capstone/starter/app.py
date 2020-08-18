import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import models
import json

def cprint(label, data):
	print("")
	print(label)
	print(data)
	print("")

def json_formatter(model, data):
	json_formatted = []

	if model == "Movies":
		for x in data:
			new_dict = {"id": str(x.id), "title": x.title, "release_date": str(x.release_date)}
			json_formatted.append(new_dict)
	elif model == "Actor":
		for x in data:
			new_dict = {"id": str(x.id), "name": x.name, "age": str(x.age), "gender": x.gender}
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

	
# =========================================================================
# 								ACTOR ROUTES
# =========================================================================

	# ++++++++++++++++++++++ GET ACTORS ++++++++++++++++++++++
	@app.route('/actors', methods=['GET'])
	def get_actors():    
		all_actors = models.Actor.query.all()

		formatted_response = json_formatter("Actor", all_actors)
		cprint("formatted_response", formatted_response)

		return formatted_response


# =========================================================================
# 								MOVIE ROUTES
# =========================================================================

	# ++++++++++++++++++++++ GET MOVIES ++++++++++++++++++++++
	@app.route('/movies', methods=['GET'])
	def get_movies():    
		all_movies = models.Movies.query.all()

		formatted_response = json_formatter("Movies", all_movies)
		cprint("formatted_response", formatted_response)

		return formatted_response

	return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)