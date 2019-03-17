import pytest

from flask_script import Manager, Command
from sqlalchemy import create_engine

from sqlalchemy_utils import database_exists, create_database

import private_config
from extensions import flask_db as db
from private_config import JACOB_TEMPORARY_EMAIL, JACOB_TEMPORARY_ACCOUNT_PASSWORD, MARLEN_TEMPORARY_EMAIL, \
    MARLEN_TEMPORARY_ACCOUNT_PASSWORD
from undyingkingdoms import app
from undyingkingdoms.models import World, Kingdom, County, User
from undyingkingdoms.models.forum import Forum, Thread
from undyingkingdoms.models.preferences import Preferences
from undyingkingdoms.static.metadata.metadata import kingdom_names

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
    with app.app_context():
        # Create the game world
        world = World()
        world.save()

        # Create all the kingdoms
        for i in range(len(kingdom_names)):
            kingdom = Kingdom(kingdom_names[i])
            kingdom.save()

        # Create Elthran
        user = User("elthran", JACOB_TEMPORARY_EMAIL, JACOB_TEMPORARY_ACCOUNT_PASSWORD)
        user.is_admin = True
        user.is_active = True
        user.save()
        county = County(1, "Ulthuan", "Elthran", user.id, 'Goblin', 'Sir', 'Merchant')
        county.save()
        county.vote = county.id
        county.kingdom_id = 1
        county.buildings['arcane'].total = 5
        county.technologies['arcane knowledge I'].completed = True
        county.technologies['arcane knowledge II'].completed = True
        county.technologies['arcane knowledge III'].completed = True
        county.mana = 500
        county.happiness = 80
        preferences = Preferences(county.id, user.id)
        preferences.save()
        aldoroth = Kingdom.query.get(1)
        aldoroth.leader = county.id

        # Create Haldon
        user = User("haldon", MARLEN_TEMPORARY_EMAIL, MARLEN_TEMPORARY_ACCOUNT_PASSWORD)
        user.is_admin = True
        user.is_active = True
        user.save()
        county = County(1, "Northern Wastes", "Haldon", user.id, 'Dwarf', 'Sir', 'Merchant')
        county.save()
        county.vote = county.id
        county.kingdom_id = 2
        county.buildings['arcane'].total = 5
        county.technologies['arcane knowledge I'].completed = True
        county.technologies['arcane knowledge II'].completed = True
        county.technologies['arcane knowledge III'].completed = True
        county.mana = 500
        county.happiness = 80
        county.iron = 200
        county.buildings['lair'].total = 1

        preferences = Preferences(county.id, user.id)
        preferences.save()
        faenoth = Kingdom.query.get(2)
        faenoth.leader = county.id

        # Create AI1 (He is weak and easier to attack for testing)
        user = User("ai1", "1@gmail.com", "star")
        user.save()
        county = County(1, "Robotica1", "Mr. Roboto1", user.id, 'Dwarf', 'Lady', 'Engineer')
        county.save()
        county.vote = county.id
        county.armies['peasant'].amount = 0
        county.armies['archer'].amount = 0
        preferences = Preferences(county.id, user.id)
        preferences.save()

        # Create AI2 (He is weak and easier to attack for testing)
        user = User("ai2", "2@gmail.com", "star")
        user.save()
        county = County(2, "Robotica2", "Mr. Roboto2", user.id, 'Elf', 'Lady', 'Engineer')
        county.save()
        county.vote = county.id
        county.armies['peasant'].amount = 0
        county.armies['archer'].amount = 0
        preferences = Preferences(county.id, user.id)
        preferences.save()

        # Create AI3 (He is weak and easier to attack for testing)
        user = User("ai3", "3@gmail.com", "star")
        user.save()
        county = County(2, "Robotica3", "Mr. Roboto3", user.id, 'Human', 'Lady', 'Engineer')
        county.save()
        county.vote = county.id
        county.kingdom_id = 3
        county.armies['peasant'].amount = 0
        county.armies['archer'].amount = 0
        preferences = Preferences(county.id, user.id)
        preferences.save()

        # Create Forum shell
        forum = Forum()
        forum.save()
        thread = Thread(forum.id, "General", 1)
        thread.save()
        thread = Thread(forum.id, "Feedback & Suggestions", 1)
        thread.save()
        thread = Thread(forum.id, "Bug Reports", 1)
        thread.save()
        thread = Thread(forum.id, "Weekly Art Competition", 1)
        thread.save()
        thread = Thread(forum.id, "Monthly Feature Vote", 1)
        thread.save()

        db.session.commit()
    print("Rebuilt all meta-data users.")


@manager.command
def reset_db():
    """Drops then rebuilds the database."""
    # os.system('mysql --defaults-file=private_mysql_config.cnf -e "DROP DATABASE IF EXISTS {name};"'.format(
    #         name=private_config.DATABASE_NAME))
    #     print("Database deleted!")
    #     os.system(
    #         'mysql --defaults-file=private_mysql_config.cnf -e '
    #         '"CREATE DATABASE IF NOT EXISTS {name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"'.format(
    #             name=private_config.DATABASE_NAME))
    #     print("Database recreated!")
    engine = create_engine(private_config.SQLALCHEMY_DATABASE_URI)
    if not database_exists(engine.url):
        create_database(engine.url)
    drop_db()
    init_db()
    populate_db()
    print("Database recreated!")


if __name__ == '__main__':
    manager.run()
