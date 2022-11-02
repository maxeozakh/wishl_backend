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
