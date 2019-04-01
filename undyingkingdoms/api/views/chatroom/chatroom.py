from datetime import datetime

from flask import jsonify, request
from flask.views import MethodView
from flask_login import login_required, current_user

from undyingkingdoms.models import Chatroom
from undyingkingdoms.models.forms.message import MessageForm


class ChatroomAPI(MethodView):
    @login_required
    def get(self):
        form = MessageForm()
        chat = Chatroom.query.filter_by(kingdom_id=current_user.county.kingdom_id).all()
        current_user.county.preferences.last_checked_townhall = datetime.utcnow()  # Update that user has looked at town hall
        return jsonify(
            status="success",
            message=f"You called on {__name__}",
            form=form,
            chat=chat,
            globalChatOn=current_user.global_chat_on
        )

    @login_required
    def post(self):
        form = MessageForm()

        current_user.county.preferences.last_checked_townhall = datetime.utcnow()  # Update that user has looked at town hall

        is_global = request.form['isGlobal'] == 'true'
        update_only = request.form['updateOnly'] == 'true'
        current_user.global_chat_on = is_global

        if update_only:
            if is_global:
                chat = Chatroom.query.filter_by(is_global=True).all()
            else:
                chat = Chatroom.query.filter_by(kingdom_id=current_user.county.kingdom_id, is_global=False).all()
            return jsonify(
                status='success',
                message='Here is the latest data.',
                data=(message.json_ready() for message in chat),
                csrf=form.csrf_token.current_token,
            )
        elif form.validate_on_submit():
            message = Chatroom(current_user.county.kingdom_id, current_user.county.id, form.content.data, is_global=is_global)
            message.save()
            return jsonify(
                status='success',
                message='Here is your message.',
                data=message.json_ready(),
            )
        return jsonify(
            status='fail',
            message='Did not pass form validation.'
        )
