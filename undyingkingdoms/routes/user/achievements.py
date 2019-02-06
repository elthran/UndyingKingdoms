from flask import render_template, redirect
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from undyingkingdoms import app, db
from undyingkingdoms.models import Achievement
from undyingkingdoms.routes.helpers import in_active_session


@app.route('/user/achievements/', methods=['GET', 'POST'])
@mobile_template('{mobile/}user/achievements.html')
@login_required
@in_active_session
def achievements(template):
    all_achievements = Achievement.query.filter_by(user_id=current_user.id).all()
    return render_template(template, achievements=all_achievements)
