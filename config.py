import os
import psycopg2

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret'
	# Allows me to work with a PostgreSQl db
	DATABASE_URI = os.environ['DATABASE_URL']
	SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	# Handle logs
	LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')