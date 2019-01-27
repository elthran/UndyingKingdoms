from flask import url_for, redirect, render_template
from flask_login import current_user
from flask_login import login_user
from flask_mobility.decorators import mobile_template

from undyingkingdoms import app, User
from undyingkingdoms.models import Session
from undyingkingdoms.models.forms.register import RegisterForm


@app.route('/register/', methods=['GET', 'POST'])
@mobile_template('{mobile/}index/register.html')
def register(template):
    form = RegisterForm()
    if current_user.is_authenticated:
        return redirect(url_for('overview', kingdom_id=current_user.county.kingdom.id, county_id=current_user.county.id))
    if form.validate_on_submit() and not User.query.filter_by(email=form.email.data).first():
        user = User(form.username.data, form.email.data, form.password.data)
        user.save()
        session = Session(user_id=user.id)
        session.save()
        login_user(user)
        # Right ow it immediately logs you in.
        # In the future it will send you an email for confirmation first.
        session = Session(user_id=user.id)
        session.save()
        return redirect(url_for('initialize'))
    return render_template(template, form=form)
