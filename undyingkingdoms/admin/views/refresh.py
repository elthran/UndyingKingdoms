from flask import jsonify, current_app
from flask.views import MethodView
from flask_login import current_user, logout_user

from extensions import flask_db as db
from .. import helpers
from undyingkingdoms.models import World, User


class RefreshAPI(MethodView):
    def get(self):
        """Refresh game play by advancing the current age."""
        users = User.query.all()
        for user in users:
            user.ages_completed += 1
        world = World.query.first()
        world.advance_age()
        self.refresh_age()
        # If the current user doesn't get logged out,
        # it's buggy when they reload the game (as they are logged in with no county)
        current_user.in_active_session = False
        logout_user()
        return jsonify(status='success',
                       message='Game age has been advanced and world data has been reset.'), 200

    @staticmethod
    def refresh_age():
        """Reset the current age by delete non user or metadata tables.
        This should delete all game data, but not user or meta_data. Delete the tables below and then rebuild them.
        Consider moving this to a "service" module.
        """
        tables = ['county', 'army', 'building', 'notification', 'expedition']
        current_app.logger.info("Refreshing tables:")
        for table in tables:
            helpers.empty_table(db.engine, table)
            current_app.logger.info("Truncating table `{}`.".format(table))
