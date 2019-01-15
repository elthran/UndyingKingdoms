from flask.views import MethodView

from .helpers import check_clock_key
from undyingkingdoms.models import World


class EndAgeAPI(MethodView):
    @check_clock_key
    def get(self):
        # advance game clock here!
        world = World.query.first()
        world.end_age()

        # update age, day
        world.advance_age()
