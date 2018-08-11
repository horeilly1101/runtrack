from runtrack_app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import INTEGER, TEXT, TIMESTAMP
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
	id = db.Column(INTEGER, primary_key=True, index=True)
	email = db.Column(TEXT, unique=True)
	name = db.Column(TEXT)
	password_hash = db.Column(TEXT)
	created_at = db.Column(TIMESTAMP, default=datetime.utcnow)

	def __repr__(self):
		return "<User {}>".format(self.name)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

class Run(db.Model):
	id = db.Column(INTEGER, primary_key=True, index=True)
	# All distances stored in kilometers
	distance = db.Column(TEXT)
	started_at = db.Column(TIMESTAMP)
	ended_at = db.Column(TIMESTAMP)

	def __repr__(self):
		return "<Run {}km>".format(self.distance)