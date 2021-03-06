"""
database model classes:
	User: user model
	Run: run model
	Goal: goal model
"""

from datetime import datetime

from sqlalchemy.dialects.postgresql import INTEGER, TEXT, TIMESTAMP, DATE
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from runtrack.models import db, login


class User(UserMixin, db.Model):
	"""model that describes a user of the app"""
	id = db.Column(INTEGER, primary_key=True, index=True)
	email = db.Column(TEXT, unique=True)
	name = db.Column(TEXT)
	password_hash = db.Column(TEXT)
	created_at = db.Column(TIMESTAMP, default=datetime.utcnow)

	runs = db.relationship("Run", backref="user", lazy=True, cascade="save-update, merge, delete")
	goals = db.relationship("Goal", backref="user", lazy=True, cascade="save-update, merge, delete")

	def __repr__(self):
		return "<User {}>".format(self.name)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)


class Run(db.Model):
	id = db.Column(INTEGER, primary_key=True, index=True)
	user_id = db.Column(INTEGER, db.ForeignKey("user.id"), index=True)
	distance = db.Column(TEXT)
	date = db.Column(DATE)

	def __repr__(self):
		return "<Run {} miles>".format(self.distance)


class Goal(db.Model):
	id = db.Column(INTEGER, primary_key=True, index=True)
	user_id = db.Column(INTEGER, db.ForeignKey("user.id"), index=True)
	distance = db.Column(TEXT)
	date = db.Column(DATE)

	def __repr__(self):
		return "<Goal {} miles>".format(self.distance)


@login.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))