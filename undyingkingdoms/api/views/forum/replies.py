from flask import jsonify, request
from flask.views import MethodView
from flask_login import login_required

from undyingkingdoms.api.vue_safe import vue_safe_post
from undyingkingdoms.models.forum import Post


class RepliesAPI(MethodView):
    def get(self):
        post_id = request.args.get('post_id', 0, int)
        post = Post.query.get(post_id)
        replies = Post.query.filter_by(parent_post_id=post_id).all()
        return jsonify(
            post=vue_safe_post(post),
            replies=[vue_safe_post(reply) for reply in replies]
        )
