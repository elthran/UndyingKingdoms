from datetime import datetime

from flask import render_template, url_for, redirect, jsonify, make_response
from flask.views import MethodView
from flask_login import login_required, current_user

from undyingkingdoms import app, global_chatroom
from undyingkingdoms.models.forms.chatroom import ChatForm


# @app.route('/gameplay/chatroom/', methods=['GET', 'POST'])
# @login_required
# def chatroom():
#     if not current_user.in_active_session:
#         current_user.in_active_session = True
#     chat_id = current_user.county.kingdom.id
#     if current_user.county.kingdom.id not in global_chatroom:
#         global_chatroom[chat_id] = []
#     form = ChatForm()
#     if form.validate_on_submit():
#         global_chatroom[chat_id].append((str(datetime.now())[10:19], current_user.county.leader, form.message.data))
#         global_chatroom[chat_id] = global_chatroom[chat_id][-20:]  # Only keeps most recent 20 items
#         return redirect(url_for('chatroom'))
#     return render_template('gameplay/chatroom.html', form=form, chat=global_chatroom[chat_id])


class ChatRoomAPI(MethodView):
    @login_required
    def get(self):
        app.logger.critical("Reached get method.")
        if not current_user.in_active_session:
            current_user.in_active_session = True
        chat_id = current_user.county.kingdom.id
        if current_user.county.kingdom.id not in global_chatroom:
            global_chatroom[chat_id] = []
        form = ChatForm()
        return render_template('gameplay/chatroom.html', form=form, chat=global_chatroom[chat_id])

    @login_required
    def post(self):
        if not current_user.in_active_session:
            current_user.in_active_session = True
        chat_id = current_user.county.kingdom.id
        form = ChatForm()
        if form.validate_on_submit():
            global_chatroom[chat_id].append((str(datetime.now())[10:19], current_user.county.leader, form.message.data))
            global_chatroom[chat_id] = global_chatroom[chat_id][-20:]  # Only keeps most recent 20 items
            return jsonify(dict(
                status='success',
                message='Here is your chat data.',
                data=global_chatroom,
            ))
        return jsonify(dict(
            status='fail',
            message='Did not pass form validation.'
        ))
