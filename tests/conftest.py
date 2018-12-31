import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

import config
from undyingkingdoms import app, flask_db


@pytest.fixture
def client():
    app.config.from_object(config.TestingConfig)
    test_db = flask_db
    client = app.test_client()

    engine = create_engine(config.TestingConfig.SQLALCHEMY_DATABASE_URI)
    if not database_exists(engine.url):
        create_database(engine.url)

    with app.app_context():
        test_db.drop_all()
        test_db.create_all()

    yield client

    with app.app_context():
        test_db.drop_all()
