from flask import url_for, redirect, render_template
from flask_login import current_user
from flask_login import login_user

from undyingkingdoms import app, User, db
from undyingkingdoms.models.analytics import AuthenticationEvent
from undyingkingdoms.models.bases import GameEvent
from undyingkingdoms.models.forms.login import LoginForm
from undyingkingdoms.models.forms.register import RegisterForm


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if current_user.is_authenticated:
        return redirect(url_for('overview'))
    if form.validate_on_submit() and not User.query.filter_by(email=form.email.data).first():
        user = User(form.username.data, form.email.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        authentication_event = AuthenticationEvent(user_id=user.id,
                                                   activity="registration",
                                                   session_id=user.session_id)
        db.session.add(authentication_event)
        db.session.commit()
        login_user(user)
        return redirect(url_for('initialize'))
    return render_template("index/register.html", form=form)
