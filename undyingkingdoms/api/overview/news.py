from flask import jsonify
from flask.views import MethodView
from flask_login import login_required, current_user

from undyingkingdoms.serializers.vue_safe import vue_safe_news


class NewsAPI(MethodView):
    @login_required
    def get(self):
        county = current_user.county

        return jsonify(
            status="success",
            debugMessage=f"You called on {__name__}",
            news=vue_safe_news(county.display_news()),
            oldNews=vue_safe_news(county.display_old_news())
        )
