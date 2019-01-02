from flask import jsonify, current_app
from flask.views import MethodView

from extensions import flask_db as db
from .. import helpers
from undyingkingdoms.models import World


class RefreshAPI(MethodView):
    def get(self):
        """Refresh game play by advancing the current age."""
        world = World.query.first()
        world.advance_age()
        self.refresh_age()

        return jsonify(
            status='success',
            message='Game age has been advanced and world data has been reset.'
        ), 200

    def refresh_age(self):
        """Reset the current age by delete non user or metadata tables.

                This should delete all game data, but not user or meta_data. Delete the tables below and then rebuild them.

                Consider moving this to a "service" module.
        """
        tables = ['county', 'army', 'building', 'notification', 'expedition']
        current_app.logger.info("Refreshing tables:")
        for table in tables:
            helpers.empty_table(db.engine, table)
            current_app.logger.info("Truncating table `{}`.".format(table))
