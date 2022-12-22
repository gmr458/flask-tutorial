"""Module database"""

from flask import current_app, g, Flask
import pymysql
import pymysql.cursors


def get_mysql_connection():
    """Get connection to the MySQL database."""
    if "connection" not in g:
        g.connection = pymysql.connect(
            host=current_app.config["MYSQL_HOST"],
            user=current_app.config["MYSQL_USER"],
            password=current_app.config["MYSQL_PASSWORD"],
            database=current_app.config["MYSQL_DATABASE"],
            cursorclass=pymysql.cursors.DictCursor,
        )

    return g.connection


def close_mysql_connection(e=None) -> None:
    """Close connection to the MySQL database."""
    connection = g.pop("connection", None)

    if connection is not None:
        connection.close()


def init_app(app: Flask) -> None:
    """Register close_mysql_connection() with the application."""

    # Flask instance app call the function close_mysql_connection()
    # when cleaning up after returning the response
    app.teardown_appcontext(close_mysql_connection)
