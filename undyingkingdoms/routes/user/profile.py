from flask import render_template, redirect
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from undyingkingdoms import app, db
from undyingkingdoms.models import Achievement


@app.route('/user/profile/', methods=['GET', 'POST'])
@mobile_template('{mobile/}user/profile.html')
@login_required
def profile(template):
    return render_template(template, user=current_user)
