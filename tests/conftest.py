import pytest
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

import config
from undyingkingdoms import app as udk_app, flask_db
from utilities.testing_objects import build_testing_objects


@pytest.fixture(scope="session")
def app():
    """Create and configure a new app instance for each test."""
    app = udk_app  # fixing naming overlap.
    app.config.from_object(config.TestingConfig)  # overwrite dev config.

    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    if not database_exists(engine.url):
        create_database(engine.url)

    with app.app_context():
        flask_db.drop_all()
        flask_db.create_all()
        # Create the game world
        objs = build_testing_objects()
        flask_db.session.commit()

    yield app
    app.config['SQLALCHEMY_ECHO'] = False

    with app.app_context():
        flask_db.drop_all()


@pytest.fixture(scope='module')
def build(app):
    with app.app_context():
        flask_db.drop_all()
        flask_db.create_all()
        # Create the game world
        objs = build_testing_objects()
        flask_db.session.commit()
        return objs


@pytest.fixture
def ctx(app):
    with app.app_context() as ctx:
        yield ctx


@pytest.fixture
def client(app):
    """A test client for the app."""
    with app.test_client() as client:
        yield client

# @pytest.fixture
# def logger():
#     logging.basicConfig(level=logging.DEBUG)
#     yield logging.getLogger('default')
