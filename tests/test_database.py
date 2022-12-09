"""Module test_database flaskr"""

import sqlite3

import pytest
from flaskr.database import get_database


def test_get_close_database(app):
    with app.app_context():
        database = get_database()
        assert database is get_database()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        database.execute("SELECT 1")

    assert "closed" in str(e.value)


def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr("flaskr.database.init_db", fake_init_db)
    result = runner.invoke(args=["init-db"])
    assert "Initialized the database." in result.output
    assert Recorder.called
