from flask.views import MethodView

from .helpers import check_clock_key
from undyingkingdoms.models.exports import World


class AdvanceAgeAPI(MethodView):
    @check_clock_key
    def get(self):
        # advance game clock here!
        world = World.query.first()
        # update age, day
        world.advance_age()
