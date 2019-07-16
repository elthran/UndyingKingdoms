from flask.views import MethodView

from .helpers import check_clock_key
from app.models.exports import World


class AdvanceDayAPI(MethodView):
    @check_clock_key
    def get(self):
        # advance game clock here!
        world = World.query.first()
        world.advance_day()
