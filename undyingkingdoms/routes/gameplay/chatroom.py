from flask import render_template
from flask_login import login_required, current_user

from undyingkingdoms import app
from undyingkingdoms.models.forms.chatroom import ChatForm


@login_required
@app.route('/gameplay/chatroom/', methods=['GET', 'POST'])
def chatroom():
    form = ChatForm()
    if form.validate_on_submit():
        current_user.county.kingdom.chatroom.append(form.message.data)
    return render_template('gameplay/chatroom.html', form=form)
