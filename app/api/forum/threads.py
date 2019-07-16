from flask import jsonify
from flask.views import MethodView
from flask_login import login_required

from app.serializers.vue_safe import vue_safe_thread
from app.models.forum import Thread


class ThreadsAPI(MethodView):
    @login_required
    def get(self):
        threads = Thread.query.all()
        return jsonify(
            threads=[vue_safe_thread(thread) for thread in threads]
        )
