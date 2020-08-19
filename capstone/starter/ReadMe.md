# Project Rubric
	The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

	Models:
		Movies with attributes title and release date
		Actors with attributes name, age and gender
	
	Endpoints:
		GET /actors and /movies
		DELETE /actors/ and /movies/
		POST /actors and /movies and
		PATCH /actors/ and /movies/
	
	Roles:
		Casting Assistant
			Can view actors and movies
		Casting Director
			All permissions a Casting Assistant has and…
			Add or delete an actor from the database
			Modify actors or movies
		Executive Producer
			All permissions a Casting Director has and…
			Add or delete a movie from the database
	
	Tests:
		One test for success behavior of each endpoint
		One test for error behavior of each endpoint
		At least two tests of RBAC for each role






Todos
	Backend
		
		Todo Tuesday:
			- Review project rubric  (https://review.udacity.com/#!/rubrics/2682/view)
			- Begin writing tests for routes and corresponding routes
			- Generate test data
			- Once routes are functional, set up auth0 app and API as well as roles and permissions
