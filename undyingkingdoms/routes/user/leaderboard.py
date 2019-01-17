from flask import render_template
from flask_login import login_required, current_user

from undyingkingdoms import app, User


@login_required
@app.route('/user/leaderboard/', methods=['GET', 'POST'])
def leaderboard():
    if not current_user.in_active_session:
        current_user.in_active_session = True
    return render_template('user/leaderboard.html', users=User.query.all())
