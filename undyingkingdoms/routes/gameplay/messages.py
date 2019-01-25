from flask import render_template
from flask_login import login_required, current_user

from undyingkingdoms import app
from undyingkingdoms.models import Message


@app.route('/gameplay/messages/', methods=['GET', 'POST'])
@login_required
def messages():
    if not current_user.in_active_session:
        current_user.in_active_session = True
    new_messages = Message.query.filter_by(county_id=current_user.county.id, unread=True).all()
    for message in new_messages:
        message.unread = False
    return render_template('gameplay/messages.html')
