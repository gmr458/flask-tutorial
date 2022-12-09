"""Module flaskr."""
import os

from flask import Flask

# Database
from . import database

# Blueprints
from . import auth, blog


def create_app(test_config=None):
    """This is the application factory function, create and configure the app."""

    app = Flask(__name__, instance_relative_config=True)

    # Setting some default configuration that the app will use.
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Init the database
    database.init_app(app)

    # Register blueprints
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)

    app.add_url_rule("/", endpoint="index")

    return app
