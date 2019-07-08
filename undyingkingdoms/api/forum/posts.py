from flask import jsonify, request
from flask.views import MethodView
from flask_login import login_required, current_user

from undyingkingdoms.serializers.vue_safe import vue_safe_post, vue_safe_thread
from undyingkingdoms.models.forms.message import MessageForm
from undyingkingdoms.models.forum import Post, Thread


class PostsAPI(MethodView):
    @login_required
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
        post_id = request.args.get('post_id', 0, type=int)
        thread_id = request.args.get('thread_id', type=int)
        if form.validate_on_submit():
            post = Post(thread_id, current_user.id, form.title.data, form.content.data, post_id)
            post.save()
            return jsonify(
                debugMessage='Your post was saved.',
            ), 201
        return jsonify(
            debugMessage='Failed form validation.'
        ), 400
