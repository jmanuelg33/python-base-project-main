import pytest

import flask_migrate
from src import create_app
from src.app import CONFIG
from src import db as _db

from .fixtures import *

TEST_CONFIG = CONFIG | {
    'TESTING': True,
    'DEBUG': True
}


@pytest.fixture(scope="session")
def app():
    app = create_app(config=TEST_CONFIG)
    with app.app_context():
        yield app


@pytest.fixture(scope="function")
def test_client(app):
    return app.test_client()


@pytest.fixture(scope="session")
def db(app, request):
    """Session-wide test database."""

    def teardown():
        flask_migrate.downgrade(revision='base', directory="src/database/migrations")

    _db.app = app

    flask_migrate.upgrade(directory="migrations")
    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope="function")
def session(db, request):
    db.session.begin_nested()

    def commit():
        db.session.flush()

    # patch commit method
    old_commit = db.session.commit
    db.session.commit = commit

    def teardown():
        db.session.rollback()
        db.session.close()
        db.session.commit = old_commit

    request.addfinalizer(teardown)
    return db.session
