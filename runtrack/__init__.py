"""Module that contains the runtrack app."""

from flask import Flask
from config import Config

from runtrack.models import db, migrate, login, tables
from runtrack.controllers.auth import auth
from runtrack.controllers.main import main
from runtrack.controllers.errors import errors


def create_app():
    """Application factory for the runtrack app.
    :return: runtrack app
    """
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(Config)

    # add extensions
    db.init_app(app)
    login.init_app(app)
    migrate.init_app(app, db)

    # add routes
    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
