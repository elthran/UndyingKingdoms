from flask import render_template
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from undyingkingdoms import app
from undyingkingdoms.models import Message
from undyingkingdoms.routes.helpers import in_active_session


@app.route('/gameplay/messages/', methods=['GET', 'POST'])
@mobile_template('{mobile/}gameplay/messages.html')
@login_required
@in_active_session
def messages(template):
    new_messages = Message.query.filter_by(county_id=current_user.county.id, unread=True).all()
    for message in new_messages:
        message.unread = False
    return render_template(template)
