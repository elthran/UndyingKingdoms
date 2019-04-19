from flask import jsonify, url_for
from flask.views import MethodView
from flask_login import login_required

class RoutingAPI(MethodView):
    @login_required
    def get(self):
        return jsonify(
            root=url_for('forum', thread_id=0, post_id=0)[:-4]
        )
