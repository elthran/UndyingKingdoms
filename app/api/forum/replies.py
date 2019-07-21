from importlib import import_module

from flask import jsonify, request
from flask.views import MethodView
from flask_login import login_required

from app.serializers.vue_safe import vue_safe_post, vue_safe_reply
get_forum = lambda: import_module('app.models.forum')


class RepliesAPI(MethodView):
    @login_required
    def get(self):
        forum = get_forum()
        post_id = request.args.get('post_id', 0, int)
        post = forum.Post.query.get(post_id)
        replies = forum.Post.query.filter_by(parent_post_id=post_id).all()
        json_post = vue_safe_post(post)
        return jsonify(
            post=json_post,
            replies=[json_post] + [vue_safe_reply(reply) for reply in replies]
        )
