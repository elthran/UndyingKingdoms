import os
import logging

import pytest
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

import config
from undyingkingdoms import app, flask_db, User
from undyingkingdoms.models import World, Kingdom, County
from undyingkingdoms.static.metadata import kingdom_names


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
        # Create the game world
        world = World()
        world.save()

        # Create all the kingdoms
        for i in range(len(kingdom_names)):
            kingdom = Kingdom(kingdom_names[i])
            kingdom.save()

        # Create Haldon
        user = User("haldon", "haldon@gmail.com", "brunner")
        user.is_admin = True
        user.is_active = True
        user.save()
        county = County("Northern Wastes", "Haldon", user.id, 'Dwarf', 'Male')
        county.save()
        county.vote = county.id
        test_db.session.commit()

    yield client

    with app.app_context():
        test_db.drop_all()


# @pytest.fixture
# def logger():
#     logging.basicConfig(level=logging.DEBUG)
#     yield logging.getLogger('default')
