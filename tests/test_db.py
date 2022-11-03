import sqlite3

import pytest
from wishl.db import get_db


def test_get_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()


def test_close_db(app):
    with app.app_context():
        db = get_db()

    with pytest.raises(sqlite3.ProgrammingError) as error:
        db.execute('SELECT NEWBIE40000')

    assert 'closed' in str(error.value)


def test_init_db_command(runner, monkeypatch):
    global is_init_db_called
    is_init_db_called = False

    def fake_init_db():
        global is_init_db_called
        is_init_db_called = True

    monkeypatch.setattr('wishl.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'db is ready' in result.output
    assert is_init_db_called
