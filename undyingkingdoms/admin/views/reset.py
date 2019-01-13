from flask import jsonify, current_app
from flask.views import MethodView

from extensions import flask_db as db
from private_config import JACOB_TEMPORARY_ACCOUNT_PASSWORD, MARLEN_TEMPORARY_ACCOUNT_PASSWORD, JACOB_TEMPORARY_EMAIL, \
    MARLEN_TEMPORARY_EMAIL
from undyingkingdoms.models.forum import Forum, Thread
from .. import helpers
from undyingkingdoms.models import User, County, Kingdom, World
from undyingkingdoms.static.metadata import kingdom_names


class ResetAPI(MethodView):
    # currently can use login_required as flask-login requires user table.
    # @login_required
    def get(self):
        # Should make it so only admin can visit
        current_app.logger.info("Deleting tables:")
        for table in db.metadata.tables.keys():
            helpers.delete_table(db.engine, table)
            current_app.logger.info("Dropped table `{}`.".format(table))
        current_app.logger.info("Creating tables:")
        db.create_all()

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
        county = County("Ulthuan", "Elthran", user.id, 'Human', 'Male')
        county.save()
        county.vote = county.id

        # Create Haldon
        user = User("haldon", MARLEN_TEMPORARY_EMAIL, MARLEN_TEMPORARY_ACCOUNT_PASSWORD)
        user.is_admin = True
        user.is_active = True
        user.save()
        county = County("Northern Wastes", "Haldon", user.id, 'Dwarf', 'Male')
        county.save()
        county.vote = county.id

        # Create AI (He is weak and easier to attack for testing)
        user = User("ai", "ai@gmail.com", "star")
        user.save()
        county = County("Robotica", "Mr. Roboto", user.id, 'Dwarf', 'Female')
        county.save()
        county.vote = county.id
        county.armies['peasant'].amount = 0
        county.armies['archer'].amount = 0
        
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

        return jsonify(
            status='success',
            message="Database has been deleted and rebuilt."
        ), 200
