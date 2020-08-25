# ReadMe
	Welcome to my Udacity Fullstack Nanodegree Capstone project.  This is a RESTful API designed to help manage a fictitious casting agency and uses Auth0 authentication to provide role based access to its various endpoints.  Please read through the rest of the document to find pertinent information for testing and using this API.

# Motivation
	The intent of this project is simply to sharpen my skills with Flask based APIs and user authentication.


# Deployment Testing instructions
	You can test this API by using the included Postman suite to test each Heroku endpoint, which is deployed at https://udacity-capstone-api.herokuapp.com/
			- Download the testing suite JSON file from this repo and import it into Postman
			- Tokens are already provided for each level of access and endpoints are setup to test the Heroku deployment so simply run the suite or test each endpoint manually

# Dependencies
	- Python 3.8.2
	- Flask 1.0.2
	- PostgreSQL 12.2
	- virtualenv 20.0.25


# Local Testing Instructions
	- If you have not already done so, copy this project repo to your machine in order to test the project on a local server.
	- Open a new terminal at the project directory
	- Create a new virtual environment within the project using the following command "virtualenv env"
	- Activate your virtual environment using the command "source env/bin/activate"
	- To install all project dependencies, run the command "pip -r install requirements.txt".  This will reference the requirements.txt file and install all packages listed.
	- With Postgres already installed on your machine, create a db with the command "createdb casting_agency"
	- Initialize your database with the following three commands
		- python manage.py db init
        - python manage.py db migrate
        - python manage.py db upgrade
	- Next, set up your environment variables by executing the setup.sh file with the following command: "./setup.sh"
		- In the event that this file is not executable, run "chmod 755 setup.sh" first and then run "./setup.sh"
		- This file sets a path to your new database, which should be "postgres://localhost:5432/casting_agency", but this may vary depending on where postgres is installed in your personal machine
	- You can now start your local server with the following three lines in a new terminal tab that is within the virtual environment
		- export FLASK_APP=app.py
		- export FLASK_ENV=development
		- flask run --reload
	- Your local server should now be running at http://127.0.0.1:5000/
	- You can test the endpoints by either using the included Postman suite (ensure to change the base URL for every call to http://127.0.0.1:5000/) or by running "python test_app.py" from your terminal
		- The second command will execute the unit test file included in this project, which includes tests for ever endpoint at every level of authentication

# Authentication
	Tokens for each all three roles can be found in the config.py file.


# List of endpoints
	- Base URL: https://udacity-capstone-api.herokuapp.com/
		- GET /actors
			- Returns a list of all actors listed in the Actor table
		- POST /actors
			- Enables adding new actors to the Actor table by passing the record into the body of the call
			- Example Body: {
							    "name": "Postman Test",
							    "age": "105",
							    "gender": "Female"
							}
		- PATCH /actor/<int:actor_id>
			- Enables updating a record in the Actor table by passing the record's ID into the URL and the desired updates as the body
			- Example Body: {
						        "name": "Charlize Theron",
						        "age": "45",
						        "gender": "Female"
						    }
		- DELETE /actor/<int:actor_id>/delete
			- Removes a record from the Actor table by passing the record's ID into the URL
		- GET /movies
			- Returns a list of all movies listed in the Movies table
		- POST /movies
			- Enables the creation of a new record in the Movies table by passing the new record data into the body of the call
			- Example Body: {
							    "title": "Postman Test Movie",
							    "release_date": "2020-08-17 21:14:47.095967"
							}
		- PATCH /movies/<int:movie_id>
			- Enables updating a record in the Movies table by passing the record's ID into the URL and the desired updates as the body
			- Example Body: {
						        "title": "The Machinist: Updated",
						        "release_date": "2021-08-17 21:14:47.095967"
						    }
		- DELETE /movie/<int:movie_id>/delete
			- Removes a record from the Movies table by passing the record's ID into the URL

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

	In the event that you attempt to access an endpoint that is not listed under your corresponding role above, you should expect a 403: Forbidden error.

# Generating new Tokens
	In the event that you need to generate new user tokens, you can run the following commands while your virtual environment is active
		- "python get_token.py"
			- This file will return JWT tokens for all three levels of access as well as set them as environment variables
