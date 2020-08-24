# ReadMe
	Welcome to my Udacity Fullstack Nanodegree Capstone project.  This is a RESTful API designed to help manage a fictitious casting agency and uses Auth0 authentication to provide role based access to its various endpoints.  Please read through the rest of the document to find pertinent information for testing and using this API.


# Testing instructions
	You can test this API by using the included Postman suite to test each Heroku endpoint, which is deployed at https://udacity-capstone-api.herokuapp.com/
			- Download the testing suite JSON file from this repo and import it into Postman
			- Tokens are already provided for each level of access and endpoints are setup to test the Heroku deployment so simply run the suite or test each endpoint manually

# Authentication
	Tokens for each all three roles can be found in the config.py file.


# List of endpoints
	- Base URL: https://udacity-capstone-api.herokuapp.com/
		- GET /actors
		- POST /actors
		- PATCH /actor/<int:actor_id>
		- DELETE /actor/<int:actor_id>/delete
		- GET /movies
		- POST /movies
		- PATCH /movies/<int:movie_id>
		- DELETE /movie/<int:movie_id>/delete

# Roles and Access
	1.) Assistant
			Access:
				- GET /actors
				- GET /movies
	2.) Director
			Access:
				- GET /actors
				- POST /actors
				- PATCH /actor/<int:actor_id>
				- DELETE /actor/<int:actor_id>/delete
				- GET /movies
				- PATCH /movies/<int:movie_id>
	3.) Producer
			Access:
				- GET /actors
				- POST /actors
				- PATCH /actor/<int:actor_id>
				- DELETE /actor/<int:actor_id>/delete
				- GET /movies
				- POST /movies
				- PATCH /movies/<int:movie_id>
				- DELETE /movie/<int:movie_id>/delete
			
