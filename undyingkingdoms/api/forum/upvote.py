from flask import jsonify, request
from flask.views import MethodView
from flask_login import login_required, current_user

from undyingkingdoms.models.upvotes import Upvote


class UpvoteAPI(MethodView):
    @login_required
    def get(self, post_id):
        upvote = Upvote.query.filter_by(user_id=current_user.id, post_id=post_id).first()

        try:
            upvote.toggle_vote()
            return jsonify(
                debugMessage=f"Post id:{post_id} upvote toggled for user id:{current_user.id}"
            ), 200
        except AttributeError:
            upvote = Upvote(current_user.id, post_id, 1)
            upvote.save()
            return jsonify(
                debugMessage=f"Upvote created for post id:{post_id} for user id:{current_user.id}"
            ), 201
