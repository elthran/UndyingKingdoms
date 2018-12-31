from flask import jsonify
from flask.views import MethodView

from undyingkingdoms.models import World


class RefreshAPI(MethodView):
    def get(self):
        """Refresh game play by advancing the current age."""
        world = World.query.first()
        world.advance_age()

        return jsonify(
            status='success',
            message='Game age has been advanced and world data has been reset.'
        ), 200
