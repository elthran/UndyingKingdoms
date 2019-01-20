from flask import render_template, url_for, redirect
from flask_login import login_required, current_user

from undyingkingdoms import app
from undyingkingdoms.models import Chatroom
from undyingkingdoms.models.forms.chatroom import ChatForm


@app.route('/gameplay/messages/', methods=['GET', 'POST'])
@login_required
def messages():
    if not current_user.in_active_session:
        current_user.in_active_session = True
    return render_template('gameplay/messages.html')
