from flask import render_template
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from undyingkingdoms import app, User
from undyingkingdoms.models import Kingdom


@app.route('/user/leaderboard/', methods=['GET', 'POST'])
@mobile_template('{mobile/}user/leaderboard.html')
@login_required
def leaderboard(template):
    users = User.query.all()
    current_users = [user for user in users if user.county is not None]
    counties = [user.county for user in current_users]
    kingdoms = Kingdom.query.all()
    return render_template(template, counties=counties, kingdoms=kingdoms)
