from importlib import import_module

from flask.views import MethodView

from .helpers import check_clock_key
get_models = lambda: import_module('app.models.exports')


class AdvanceAgeAPI(MethodView):
    @check_clock_key
    def get(self):
        models = get_models()
        # advance game clock here!
        world = models.World.query.first()
        # update age, day
        world.advance_age()
