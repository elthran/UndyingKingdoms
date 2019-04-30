from flask import jsonify
from flask.views import MethodView

from undyingkingdoms.models.forms.message import MessageForm


class MessagingAPI(MethodView):
    def get(self):
        form = MessageForm()
        return jsonify(
            form=dict(
                TITLE_SIZE=form.TITLE_SIZE,
                CONTENT_SIZE=form.CONTENT_SIZE,
                csrf=form.csrf_token()
            )
        )
