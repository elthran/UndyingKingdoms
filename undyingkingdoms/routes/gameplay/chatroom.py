from flask import render_template
from flask_login import login_required, current_user

from undyingkingdoms import app, g_chat_room
from undyingkingdoms.models.forms.chatroom import ChatForm


@login_required
@app.route('/gameplay/chatroom/', methods=['GET', 'POST'])
def chatroom():
    if current_user.county.kingdom.id not in g_chat_room:
        g_chat_room[current_user.county.kingdom.id] = []
    form = ChatForm()
    if form.validate_on_submit():
        g_chat_room[current_user.county.kingdom.id].append((current_user.county.leader, form.message.data))
    return render_template('gameplay/chatroom.html', form=form)
