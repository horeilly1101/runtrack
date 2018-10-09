import os
import psycopg2

class Config(object):
	# PRODUCTION
	# SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret'
	# Allows me to work with a PostgreSQl db
	# DATABASE_URL = os.environ['DATABASE_URL']
	# SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
	# conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	# SQLALCHEMY_TRACK_MODIFICATIONS = False
	# # Handle logs
	# LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

	# DEVELOPMENT
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret'
	SQLALCHEMY_DATABASE_URI = "postgresql://postgres:password@localhost:5555/postgres"
	SQLALCHEMY_TRACK_MODIFICATIONS = False