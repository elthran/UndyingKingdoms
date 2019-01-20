from flask import render_template
from flask_login import login_required, current_user

from undyingkingdoms import app


@app.route('/gameplay/messages/', methods=['GET', 'POST'])
@login_required
def messages():
    if not current_user.in_active_session:
        current_user.in_active_session = True
    return render_template('gameplay/messages.html')
