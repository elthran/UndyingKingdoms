from flask import render_template
from flask import g
from flask_login import login_required, current_user

from undyingkingdoms import app
from undyingkingdoms.models.forms.chatroom import ChatForm


@login_required
@app.route('/gameplay/chatroom/', methods=['GET', 'POST'])
def chatroom():
    if not 'chatroom' in g:
        g['chatroom'] = {current_user.county.kingdom.id: []}
    form = ChatForm()
    if form.validate_on_submit():
        # will need to add kingdom.id if it doesn't exists.
        g['chatroom'][current_user.county.kingdom.id].append((current_user.county.leader, form.message.data))
    return render_template('gameplay/chatroom.html', form=form)
