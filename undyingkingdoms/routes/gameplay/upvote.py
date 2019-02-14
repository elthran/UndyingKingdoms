from flask import jsonify
from flask.views import MethodView
from flask_login import login_required, current_user

from undyingkingdoms import app
from undyingkingdoms.models.upvotes import Upvote


class UpvoteAPI(MethodView):
    @login_required
    def get(self, post_id):
        upvote = Upvote.query.filter_by(user_id=current_user.id, post_id=post_id).first()

        try:
            upvote.toggle_vote()
            return jsonify(
                status="success",
                messaage=f"Post id:{post_id} upvote toggled for user id:{current_user.id}"
            )
        except AttributeError:
            upvote = Upvote(current_user.id, post_id, 1)
            upvote.save()
            return jsonify(
                status="success",
                message=f"Upvote created for post id:{post_id} for user id:{current_user.id}"
            )

app.add_url_rule('/user/upvote/<post_id>', view_func=UpvoteAPI.as_view('upvote_api'))
