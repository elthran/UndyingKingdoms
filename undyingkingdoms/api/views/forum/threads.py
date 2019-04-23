from flask import jsonify
from flask.views import MethodView

from undyingkingdoms.api.vue_safe import vue_safe_thread
from undyingkingdoms.models.forum import Thread


class ThreadsAPI(MethodView):
    def get(self):
        threads = Thread.query.all()
        return jsonify(
            threads=[vue_safe_thread(thread) for thread in threads]
        )
