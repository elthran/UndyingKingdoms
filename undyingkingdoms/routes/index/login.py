from flask import url_for, redirect, render_template, flash
from flask_login import current_user
from flask_login import login_user

from undyingkingdoms import app, User, db
from undyingkingdoms.models.forms.login import LoginForm
from undyingkingdoms.models.sessions import Session


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('overview', kingdom_id=current_user.county.kingdom.id, county_id=current_user.county.id))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            if current_user.county is None:
                return redirect(url_for('initialize'))
            return redirect(url_for('overview', kingdom_id=current_user.county.kingdom.id, county_id=current_user.county.id))
        else:
            flash("Your email or password was incorrect.")
    return render_template("index/login.html", form=form)
