from flask import jsonify, request
from flask.views import MethodView
from flask_login import login_required

from undyingkingdoms.api.vue_safe import vue_safe_post, vue_safe_thread
from undyingkingdoms.models.forms.message import MessageForm
from undyingkingdoms.models.forum import Post, Thread


class PostsAPI(MethodView):
    def get(self):
        thread_id = request.args.get('thread_id', 0, int)
        thread = Thread.query.get(thread_id)
        posts = Post.query.filter_by(thread_id=thread_id, parent_post_id=0).all()
        return jsonify(
            thread=vue_safe_thread(thread),
            posts=[vue_safe_post(post) for post in posts]
        )

    @login_required
    def post(self):
        form = MessageForm()
