import os
import psycopg2

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret'
	# Allows me to work with a PostgreSQl db
	DATABASE_URL = 'postgres://cxzykaabnwfehu:dd08e326f083861f06cc89c20266592a7638eed77b330f8be5c12300ba4e4b6d@ec2-54-235-86-226.compute-1.amazonaws.com:5432/d2ruk9iv8qg3ib'
	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	# Handle logs
	LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')