from flask import jsonify, request
from flask.views import MethodView
from flask_login import login_required

from undyingkingdoms.serializers.vue_safe import vue_safe_post, vue_safe_reply
from undyingkingdoms.models.forum import Post


class RepliesAPI(MethodView):
    @login_required
    def get(self):
        post_id = request.args.get('post_id', 0, int)
        post = Post.query.get(post_id)
        replies = Post.query.filter_by(parent_post_id=post_id).all()
        json_post = vue_safe_post(post)
        return jsonify(
            post=json_post,
            replies=[json_post] + [vue_safe_reply(reply) for reply in replies]
        )
