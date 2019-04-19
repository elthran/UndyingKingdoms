from flask import jsonify, request
from flask.views import MethodView
from flask_login import login_required

from undyingkingdoms.api.vue_safe import vue_safe_post
from undyingkingdoms.models.forum import Post


class PostsAPI(MethodView):
    @login_required
    def get(self):
        thread_id = request.args.get('thread_id', 0, int)
        posts = Post.query.filter_by(thread_id=thread_id, parent_post_id=0).all()
        return jsonify(
            posts=[vue_safe_post(post) for post in posts]
        )
