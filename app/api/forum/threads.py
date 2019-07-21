from importlib import import_module

from flask import jsonify
from flask.views import MethodView
from flask_login import login_required

from app.serializers.vue_safe import vue_safe_thread
get_forum = lambda: import_module('app.models.forum')


class ThreadsAPI(MethodView):
    @login_required
    def get(self):
        forum = get_forum()
        threads = forum.Thread.query.all()
        return jsonify(
            threads=[vue_safe_thread(thread) for thread in threads]
        )
