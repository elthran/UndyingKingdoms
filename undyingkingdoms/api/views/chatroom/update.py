from datetime import datetime
from distutils.util import strtobool

from flask import jsonify, request
from flask.views import MethodView
from flask_login import login_required, current_user

from undyingkingdoms.api.vue_safe import vue_safe_form
from undyingkingdoms.models import Chatroom
from undyingkingdoms.models.forms.message import MessageForm


class UpdateAPI(MethodView):
    @login_required
    def get(self):
        county = current_user.county
        preferences = current_user.preferences

        form = MessageForm()

        # return all messages, filter in frontend
        messages = Chatroom.query.filter(Chatroom.is_global, Chatroom.kingdom_id==county.kingdom_id).all()
        preferences.last_checked_townhall = datetime.utcnow()  # Update that user has looked at town hall
        return jsonify(
            debugMessage=f"You called on {__name__}",
            CSRFToken=form.csrf_token.current_token,
            messages=[m.json_ready() for m in messages],
            globalChatOn=preferences.global_chat_on,
        ), 200

    @login_required
    def post(self):
        county = current_user.county
        preferences = current_user.preferences
        form = MessageForm()

        preferences.last_checked_townhall = datetime.utcnow()  # Update that user has looked at town hall

        is_global = strtobool(request.form['global_chat_on'])
        preferences.global_chat_on = is_global

        if form.validate_on_submit():
            message = Chatroom(county.kingdom_id, county.id, form.content.data, is_global=is_global)
            message.save()
            return jsonify(
                status='success',
                debugMessage='Here is your message.',
                chatMessage=message.json_ready(),
            )
        return jsonify(
            status='success',
            debugMessage='You failed form validation but still updated chat type.'
        )
