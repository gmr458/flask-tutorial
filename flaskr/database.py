"""Module database"""

from flask import current_app, g, Flask
import pymysql
import pymysql.cursors


def get_mysql_connection():
    """Get connection to the MySQL database."""
    if "connection" not in g:
        ssl = None
        ssl_verify_identity = None

        if current_app.config["DEBUG"] is not True:
            ssl = {"ca": "/etc/ssl/cert.pem"}
            ssl_verify_identity = True

        g.connection = pymysql.connect(
            user=current_app.config["MYSQL_USER"],
            password=current_app.config["MYSQL_PASSWORD"],
            host=current_app.config["MYSQL_HOST"],
            database=current_app.config["MYSQL_DATABASE"],
            port=int(current_app.config["MYSQL_PORT"]),
            cursorclass=pymysql.cursors.DictCursor,
            ssl=ssl,
            ssl_verify_identity=ssl_verify_identity,
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
