"""Module flaskr"""

from flask import Flask

from flaskr import database, auth, blog


def create_app(test_config=None):
    """Application factory function, create and configure the app."""
    app = Flask(__name__, instance_relative_config=True)

    # Setting some default configuration that the app will use.
    app.config.from_mapping(
        SECRET_KEY="dev",
        MYSQL_HOST="localhost",
        MYSQL_USER="root",
        MYSQL_PASSWORD="Password123$",
        MYSQL_DATABASE="flaskr",
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Init the database
    database.init_app(app)

    # Register blueprints
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)

    app.add_url_rule("/", endpoint="index")

    return app
