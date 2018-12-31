from flask import jsonify
from flask.views import MethodView
from flask_login import login_required

from extensions import flask_db as db
from undyingkingdoms.models import User, County, Kingdom, World
from undyingkingdoms.static.metadata import kingdom_names


class ResetAPI(MethodView):
    # currently can use login_required as flask-login requires user table.
    # @login_required
    def get(self):
        # Should make it so only admin can visit

        print("Dropping")
        db.metadata.drop_all(db.engine)
        print("Creating")
        db.create_all()
        # Create the game world
        world = World()
        db.session.add(world)
        db.session.commit()
        # Create all the kingdoms
        for i in range(len(kingdom_names)):
            kingdom = Kingdom(kingdom_names[i])
            db.session.add(kingdom)
            db.session.commit()
        # Create AI
        user = User("ai", "ai@gmail.com", "star")
        db.session.add(user)
        db.session.commit()
        # Create AI's county
        county = County("Robotica", "Mr. Roboto", user.id, 'Human', 'Demale')
        db.session.add(county)
        db.session.commit()
        county.vote = county.id
        county.armies['peasant'].amount = 0
        db.session.commit()
        # Create Elthran
        user = User("elthran", "jacobbrunner@gmail.com", "star")
        user.is_admin = True
        user.is_active = True
        db.session.add(user)
        db.session.commit()
        # Create Elthran's county
        county = County("Ulthuan", "Elthran", user.id, 'Human', 'Male')
        db.session.add(county)
        db.session.commit()
        county.vote = county.id
        db.session.commit()
        # Create Haldon
        user = User("haldon", "haldon@gmail.com", "brunner")
        user.is_admin = True
        user.is_active = True
        db.session.add(user)
        db.session.commit()
        # Create Haldon's county
        county = County("Northern Wastes", "Haldon", user.id, 'Dwarf', 'Male')
        db.session.add(county)
        db.session.commit()
        county.vote = county.id
        db.session.commit()
        return jsonify(
            status='success',
            message="Database has been deleted and rebuilt."
        ), 200
