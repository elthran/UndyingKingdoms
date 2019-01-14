from flask.views import MethodView

from .helpers import check_clock_key
from undyingkingdoms.models import World


class AdvanceAPI(MethodView):
    @check_clock_key
    def get(self):
        # advance game clock here!
        world = World.query.first()
        world.advance_day()

        # might not be necessary
        world.game_clock = (world.game_clock + 1) % 24
