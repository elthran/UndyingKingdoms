from importlib import import_module

from flask import render_template
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from app import app
get_models = lambda: import_module('app.models.exports')


@app.route('/user/leaderboard/', methods=['GET', 'POST'])
@mobile_template('{mobile/}user/leaderboard.html')
@login_required
def leaderboard(template):
    models = get_models()
    users = models.User.query.all()
    active_users = [user for user in users if user.county is not None and user.is_bot is False]
    counties = [user.county for user in active_users if user.county is not None]
    kingdoms = models.Kingdom.query.all()
    return render_template(template, counties=counties, kingdoms=kingdoms, users=active_users)
