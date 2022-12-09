"""Module database"""

import sqlite3

import click
from flask import current_app, g, Flask


def get_database() -> sqlite3.Connection:
    """Get connection to the database."""
    if "database" not in g:
        g.database = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.database.row_factory = sqlite3.Row

    return g.database


def close_db(e=None) -> None:
    """Close connection to the database."""
    database: sqlite3.Connection = g.pop("database", None)

    if database is not None:
        database.close()


def init_db() -> None:
    """Initialize the database creating executing the SQL query from the file schema.sql"""
    database = get_database()

    with current_app.open_resource("schema.sql") as file:
        database.executescript(file.read().decode("utf8"))


@click.command("init-db")
def init_db_command() -> None:
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app: Flask) -> None:
    """Register close_db() and init_db_command() with the application."""

    # Flask instance app call the function close_db() when cleaning up after returning the response
    app.teardown_appcontext(close_db)

    # Add new command init-db that can be called with the flask command.
    app.cli.add_command(init_db_command)
