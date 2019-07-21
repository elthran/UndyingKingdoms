from importlib import import_module

from flask import jsonify, request
from flask.views import MethodView
from flask_login import login_required, current_user

from app.serializers.vue_safe import vue_safe_post, vue_safe_thread
get_forms = lambda: import_module('app.models.forms.message')
get_models = lambda: import_module('app.models.forum')


class PostsAPI(MethodView):
    @login_required
    def get(self):
        models = get_models()
        thread_id = request.args.get('thread_id', 0, int)
        thread = models.Thread.query.get(thread_id)
        posts = models.Post.query.filter_by(thread_id=thread_id, parent_post_id=0).all()
        return jsonify(
            thread=vue_safe_thread(thread),
            posts=[vue_safe_post(post) for post in posts]
        )

    @login_required
    def post(self):
        forms = get_forms()
        models = get_models()
        form = forms.MessageForm()
        post_id = request.args.get('post_id', 0, type=int)
        thread_id = request.args.get('thread_id', type=int)
        if form.validate_on_submit():
            post = models.Post(thread_id, current_user.id, form.title.data, form.content.data, post_id)
            post.save()
            return jsonify(
                debugMessage='Your post was saved.',
            ), 201
        return jsonify(
            debugMessage='Failed form validation.'
        ), 400
