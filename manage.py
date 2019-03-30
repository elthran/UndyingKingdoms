from flask_script import Manager, Command

from extensions import flask_db as db
from undyingkingdoms import app

manager = Manager(app)


@manager.add_command
class TestCommand(Command):
    """Runs unit tests.

    This should be run:
    `python manage.py test`

    or to pass argmuents to pytest
    `python manage.py test -v`
    equivalent of
    `pytest tests -v`
    """
    name = 'test'
    capture_all_args = True

    def run(self, command=None):
        import pytest
        pytest.main(['tests'] + command)


@manager.command
def init_db():
    """Initialize the database."""
    with app.app_context():
        db.create_all()
    print("Create all tables.")


@manager.command
def drop_db():
    """Drop the database."""
    db.engine.execute("SET FOREIGN_KEY_CHECKS=0;")
    with app.app_context():
        db.drop_all()
    db.engine.execute("SET FOREIGN_KEY_CHECKS=1;")
    print("Drop all tables.")


@manager.command
def populate_db():
    """Add data to the database."""
    from utilities.testing_objects import build_testing_objects

    with app.app_context():
        # Create the game world
        build_testing_objects()

        db.session.commit()
    print("Rebuilt all meta-data users.")


@manager.command
def reset_db():
    """Drops then rebuilds the database."""
    from sqlalchemy import create_engine
    from sqlalchemy_utils import database_exists, create_database

    import private_config

    engine = create_engine(private_config.SQLALCHEMY_DATABASE_URI)
    if not database_exists(engine.url):
        create_database(engine.url)
    drop_db()
    init_db()
    populate_db()
    print("Database recreated!")


if __name__ == '__main__':
    manager.run()
