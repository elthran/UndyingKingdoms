from flask import render_template, jsonify, request
from flask.views import MethodView
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from undyingkingdoms.models import Chatroom
from undyingkingdoms.models.forms.message import MessageForm
from undyingkingdoms.routes.helpers import in_active_session


class ChatRoomAPI(MethodView):
    @mobile_template('{mobile/}gameplay/chatroom.html')
    @login_required
    @in_active_session
    def get(self, template):
        form = MessageForm()
        chat = Chatroom.query.filter_by(kingdom_id=current_user.county.kingdom_id).all()
        return render_template(template, form=form, chat=chat)

    @login_required
    @in_active_session
    def post(self):
        form = MessageForm()
        chat = Chatroom.query.filter_by(kingdom_id=current_user.county.kingdom_id).all()
        if request.form['updateOnly'] == 'true':
            return jsonify(dict(
                status='success',
                message='Here is the latest data.',
                data=(message.json_ready() for message in chat),
                csrf=form.csrf_token.current_token,
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
