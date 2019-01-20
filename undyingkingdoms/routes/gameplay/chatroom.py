from flask import render_template, url_for, redirect
from flask_login import login_required, current_user

from undyingkingdoms import app
from undyingkingdoms.models import Chatroom
from undyingkingdoms.models.forms.message import MessageForm


@app.route('/gameplay/chatroom/', methods=['GET', 'POST'])
@login_required
def chatroom():
    if not current_user.in_active_session:
        current_user.in_active_session = True
    form = MessageForm()
    chat = Chatroom.query.filter_by(kingdom_id=current_user.county.kingdom_id).all()
    if form.validate_on_submit():
        message = Chatroom(current_user.county.kingdom_id, current_user.id, form.content.data)
        message.save()
        return redirect(url_for('chatroom'))
    return render_template('gameplay/chatroom.html', form=form, chat=chat)
