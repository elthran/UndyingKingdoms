from flask import jsonify, request
from flask.views import MethodView
from flask_login import login_required, current_user

from undyingkingdoms.api.vue_safe import vue_safe_thread
from undyingkingdoms.models.forum import Thread


class ThreadsAPI(MethodView):
    @login_required
    def get(self):
        threads = Thread.query.all()
        return jsonify(
            threads=[vue_safe_thread(thread) for thread in threads]
        )
