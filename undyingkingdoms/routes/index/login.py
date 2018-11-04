from flask import url_for, redirect, render_template
from flask_login import current_user
from flask_login import login_user

from undyingkingdoms import app, User, db
from undyingkingdoms.models.analytics import AuthenticationEvent
from undyingkingdoms.models.bases import GameEvent
from undyingkingdoms.models.forms.login import LoginForm


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        # If user is already logged in, don't record anything. Just send them to overview page.
        return redirect(url_for('overview'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            authentication_event = AuthenticationEvent(user_id=user.id, activity="login")
            if not authentication_event.validity:
                authentication_event = GameEvent(activity="invalid_login")
            db.session.add(authentication_event)
            db.session.commit()
            return redirect(url_for('overview'))
    return render_template("index/login.html", form=form)
