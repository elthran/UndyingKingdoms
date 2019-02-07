from flask import render_template
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from undyingkingdoms import app, User
from undyingkingdoms.routes.helpers import in_active_session


@app.route('/user/leaderboard/', methods=['GET', 'POST'])
@mobile_template('{mobile/}user/leaderboard.html')
@login_required
@in_active_session
def leaderboard(template):
    users = User.query.all()
    current_users = [user for user in users if user.county is not None]
    sorted_users = sorted(current_users, key=lambda user: user.get_current_leaderboard_score(), reverse=True)
    return render_template(template, users=sorted_users)
