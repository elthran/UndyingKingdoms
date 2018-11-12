from flask import url_for, redirect, render_template
from flask_login import current_user
from flask_login import login_user

from undyingkingdoms import app, User, db
from undyingkingdoms.models import County
from undyingkingdoms.models.analytics import AuthenticationEvent
from undyingkingdoms.models.bases import GameEvent
from undyingkingdoms.models.forms.initialize import InitializeForm
from undyingkingdoms.models.forms.login import LoginForm
from undyingkingdoms.models.forms.register import RegisterForm


@app.route('/initialize/', methods=['GET', 'POST'])
def initialize():
    form = InitializeForm()
    if form.validate_on_submit():
        county = County(form.county.data, form.leader.data, current_user.id, 1, form.race.data)
        db.session.add(county)
        db.session.commit()
        return redirect(url_for('overview'))
    return render_template("index/initialize.html", form=form)
