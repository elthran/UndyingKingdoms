from flask import render_template, jsonify, request
from flask.views import MethodView
from flask_login import login_required, current_user

from undyingkingdoms.models import Chatroom
from undyingkingdoms.models.forms.message import MessageForm


class ChatRoomAPI(MethodView):
    @login_required
    def get(self):
        if not current_user.in_active_session:
            current_user.in_active_session = True
        form = MessageForm()
        chat = Chatroom.query.filter_by(kingdom_id=current_user.county.kingdom_id).all()
        return render_template('gameplay/chatroom.html', form=form, chat=chat)

    @login_required
    def post(self):
        if not current_user.in_active_session:
            current_user.in_active_session = True
        form = MessageForm()
        chat = Chatroom.query.filter_by(kingdom_id=current_user.county.kingdom_id).all()
        if request.form['updateOnly'] == 'true':
            return jsonify(dict(
                status='success',
                message='Here is the latest data.',
                data=(message.json_ready() for message in chat)
            ))
        elif form.validate_on_submit():
            message = Chatroom(current_user.county.kingdom_id, current_user.county.id, form.content.data)
            message.save()
            return jsonify(dict(
                status='success',
                message='Here is your message.',
                data=message.json_ready(),
            ))
        return jsonify(dict(
            status='fail',
            message='Did not pass form validation.'
        ))
