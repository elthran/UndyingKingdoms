from flask import jsonify
from flask.views import MethodView

from undyingkingdoms import db
from undyingkingdoms.models import World


class RefreshAPI(MethodView):
    def get(self):
        """Refresh game play by advancing the current age."""
        world = World.query.first()
        world.advance_age()
        self.refresh_age()

    def refresh_age(self):
        """Reset the current age by delete non user or metadata tables.

                This should delete all game data, but not user or meta_data. Delete the tables below and then rebuild them.

                Consider moving this to a "service" module.
        """
        tables = [db.metadata.tables[name] for name in ['county', 'army', 'building', 'notification', 'expedition']]
        db.engine.execute('SET GLOBAL FOREIGN_KEY_CHECKS=0;')
        db.metadata.drop_all(db.engine, tables=tables)
        db.engine.execute('SET GLOBAL FOREIGN_KEY_CHECKS=1;')
        db.metadata.create_all(db.engine, tables=tables)

        return jsonify(
            status='success',
            message='Game age has been advanced and world data has been reset.'
        ), 200
