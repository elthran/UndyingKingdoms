from flask import render_template, redirect
from flask_login import login_required, current_user

from undyingkingdoms import app, db
from undyingkingdoms.models import Achievement
from undyingkingdoms.models.forum import Forum


@login_required
@app.route('/user/forum/', methods=['GET', 'POST'])
def forum():
    if not current_user.logged_in:
        current_user.logged_in = True
    the_forum = Forum.query.first()
    return render_template('user/forum.html', forum=the_forum)
