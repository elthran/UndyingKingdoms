from flask import render_template
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from app import app
from app.models.exports import Message


@app.route('/gameplay/messages/', methods=['GET', 'POST'])
@mobile_template('{mobile/}gameplay/messages.html')
@login_required
def messages(template):
    new_messages = Message.query.filter_by(county_id=current_user.county.id, unread=True).all()
    for message in new_messages:
        message.unread = False
    return render_template(template)
