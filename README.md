# runtrack

I'm building a simple web application to help me keep track of my running distances, times, and goals.

It will use:
- python3 flask to handle most of the backend features
- PostgreSQL to store data
- SQL-Alchemy to interact with the database
- Alembic to keep track of migrations
- Bootstrap4 to handle the front end

How to run on Mac OS:
- Run a local PostgreSQL database with username: "postgres", password: "password", and port: 5555.  (Of course, you could also edit `runtrack/config.py` to change any of these details.)
- Navigate to the `runtrack` directory in your Terminal.
- 
