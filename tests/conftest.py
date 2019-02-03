import pytest
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

import config
from undyingkingdoms import app as uk_app, flask_db, User
from undyingkingdoms.models import World, Kingdom, County
from undyingkingdoms.static.metadata.metadata import kingdom_names


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = uk_app  # fixing naming overlap.
    app.config.from_object(config.TestingConfig)  # overwrite dev config.
    test_db = flask_db  # we are now using a test database.

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

    yield app

    with app.app_context():
        test_db.drop_all()


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


# @pytest.fixture
# def logger():
#     logging.basicConfig(level=logging.DEBUG)
#     yield logging.getLogger('default')
