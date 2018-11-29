from flask import url_for, redirect, render_template
from flask_login import current_user
from flask_login import login_user

from undyingkingdoms import app, User, db
from undyingkingdoms.models import Session
from undyingkingdoms.models.forms.register import RegisterForm


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if current_user.is_authenticated:
        return redirect(url_for('overview', kingdom_id=current_user.county.kingdom.id, county_id=current_user.county.id))
    if form.validate_on_submit() and not User.query.filter_by(email=form.email.data).first():
        user = User(form.username.data, form.email.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        session = Session(user_id=user.id, activity="register")
        db.session.add(session)
        db.session.commit()
        login_user(user)
        # Right ow it immediately logs you in.
        # In the future it will send you an email for confirmation first.
        session = Session(user_id=user.id, activity="login")
        db.session.add(session)
        db.session.commit()
        return redirect(url_for('initialize'))
    return render_template("index/register.html", form=form)
