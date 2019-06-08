from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

from runtrack_app.models import tables
from runtrack_app.controllers.account_routes import accounts
from runtrack_app.controllers.main_routes import main
from runtrack_app.controllers.errors import errors

app.register_blueprint(accounts)
app.register_blueprint(main)
app.register_blueprint(errors)

migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
