from flask import render_template, redirect
from flask_login import login_required, current_user

from undyingkingdoms import app, db
from undyingkingdoms.models import Achievement


@login_required
@app.route('/user/achievements/', methods=['GET', 'POST'])
def achievements():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    achievements = Achievement.query.filter_by(user_id=current_user.id).all()
    return render_template('user/achievements.html', achievements=achievements)
