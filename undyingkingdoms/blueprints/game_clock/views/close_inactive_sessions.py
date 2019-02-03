from datetime import datetime

from flask.views import MethodView

from undyingkingdoms.models.users import User
from .helpers import check_clock_key


class CloseInactiveSessionsAPI(MethodView):
    @check_clock_key
    def get(self):
        for user in User.query.filter_by(_in_active_session=True).all():
            time_since_last_activity = datetime.utcnow() - user.time_modified
            if time_since_last_activity.total_seconds() > 300:  # A user who hasn't done anything in 5 minutes
                user.in_active_session = False
