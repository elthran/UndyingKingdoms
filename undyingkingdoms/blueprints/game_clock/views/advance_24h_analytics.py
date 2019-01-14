from flask.views import MethodView

from .helpers import check_clock_key
from undyingkingdoms.models import World


class Advance24hAnalyticsAPI(MethodView):
    @check_clock_key
    def get(self):
        # advance game clock here!
        world = World.query.first()
        world.advance_24h_analytics()

        # might not be necessary
        world.analytic_cycles += 1
