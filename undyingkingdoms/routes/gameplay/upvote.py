from flask import jsonify
from flask.views import MethodView
from flask_login import login_required, current_user

from undyingkingdoms.models.upvotes import Upvote
from undyingkingdoms.routes.helpers import in_active_session


class UpvoteAPI(MethodView):
    @login_required
    @in_active_session
    def get(self, post_id):
        upvote = Upvote.query.filter_by(user_id=current_user.id, post_id=post_id).first()
        if upvote is None:
            upvote = Upvote(current_user.id, post_id, 1)
            upvote.save()
        else:
            upvote.toggle_vote()

        return jsonify(
            status="succes",
            messaage="Post id:{} upvoted for user id:{}".format(post_id, current_user.id)
        )
