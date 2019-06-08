from flask import Flask
from config import Config

from runtrack_app.models import db, migrate, login, tables
from runtrack_app.controllers.account_routes import accounts
from runtrack_app.controllers.main_routes import main
from runtrack_app.controllers.errors import errors

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
login.init_app(app)
migrate.init_app(app, db)

app.register_blueprint(accounts)
app.register_blueprint(main)
app.register_blueprint(errors)
