from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()  # instantiate the database
migrate = Migrate()  # instantiate flask migration
login = LoginManager()  # instantiate the login manager
login.login_view = 'accounts.login'
