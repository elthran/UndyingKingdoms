from flask import jsonify, current_app
from flask.views import MethodView

from extensions import flask_db as db
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
        # Create AI
        user = User("ai", "ai@gmail.com", "star")
        user.save()
        # Create AI's county
        county = County("Robotica", "Mr. Roboto", user.id, 'Human', 'Demale')
        county.save()
        county.vote = county.id
        county.armies['peasant'].amount = 0
        # Create Elthran
        user = User("elthran", "jacobbrunner@gmail.com", "star")
        user.is_admin = True
        user.is_active = True
        user.save()
        # Create Elthran's county
        county = County("Ulthuan", "Elthran", user.id, 'Human', 'Male')
        county.save()
        county.vote = county.id
        # Create Haldon
        user = User("haldon", "haldon@gmail.com", "brunner")
        user.is_admin = True
        user.is_active = True
        user.save()
        # Create Haldon's county
        county = County("Northern Wastes", "Haldon", user.id, 'Dwarf', 'Male')
        county.save()
        county.vote = county.id
        
        # Create Forum shell
        forum = Forum()
        forum.save()
        thread = Thread(forum.id, "Bug Reports")
        thread.save()
        return jsonify(
            status='success',
            message="Database has been deleted and rebuilt."
        ), 200
