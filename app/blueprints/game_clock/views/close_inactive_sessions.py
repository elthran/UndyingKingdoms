from datetime import datetime
from importlib import import_module

from flask.views import MethodView

get_models = lambda: import_module('app.models.exports')
from .helpers import check_clock_key


class CloseInactiveSessionsAPI(MethodView):
    @check_clock_key
    def get(self):
        models = get_models()
        for user in models.User.query.filter_by(_in_active_session=True).all():
            time_since_last_activity = datetime.utcnow() - user.time_modified
            if time_since_last_activity.total_seconds() > 300:  # A user who hasn't done anything in 5 minutes
                user.in_active_session = False
