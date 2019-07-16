import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import DatabaseError
from sqlalchemy_utils import database_exists, create_database

import config
from extensions import flask_db as db
import app as udk
import utilities.seeds as to


def setup_app():
    """Create an configure an app."""
    app = udk.app
    app.config.from_object(config.TestingConfig)  # overwrite dev config.

    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    if not database_exists(engine.url):
        create_database(engine.url)

    with app.app_context():
        db.drop_all()
        db.create_all()
        # Create the game world
        objs = to.build_testing_objects()
        db.session.commit()

    yield (app, objs)
    app.config['SQLALCHEMY_ECHO'] = False

    with app.app_context():
        db.drop_all()


@pytest.fixture(scope="session")
def app():
    """Create and configure a new app instance for each test."""
    for udk_app, objs in setup_app():
        yield udk_app


@pytest.fixture(scope='module')
def rebuild_after(app):
    with app.app_context() as ctx:
        yield ctx
        try:
            db.session.commit()  # prevents hangs
        except DatabaseError:
            db.session.rollback()
            raise

        db.drop_all()
        db.create_all()
        # Apparently you shouldn't change the database structure while
        # the app is running. But I'm doing it.
        to.build_testing_objects()
        db.session.commit()

        # The following is temporary for testing.
        from app.models.exports import County
        assert County.query.get(1) is not None


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
