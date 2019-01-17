from flask import render_template
from flask_login import login_required, current_user

from undyingkingdoms import app


@login_required
@app.route('/user/guide/', methods=['GET', 'POST'])
def guide():
    if not current_user.in_active_session:
        current_user.in_active_session = True
    return render_template('user/guide.html')
