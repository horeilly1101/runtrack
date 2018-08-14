import os

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret'
	# Allows me to work locally with a PostgreSQl db
	SQLALCHEMY_DATABASE_URI = "postgresql://postgres:password@localhost:5555/postgres"
	SQLALCHEMY_TRACK_MODIFICATIONS = False