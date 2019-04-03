from flask import url_for, redirect, render_template
from flask_login import current_user
from flask_login import login_user
from flask_mobility.decorators import mobile_template

from undyingkingdoms import app, User
from undyingkingdoms.models.forms.activate import EmailVerificationForm


@app.route('/activate/', methods=['GET', 'POST'])
@mobile_template('{mobile/}index/activate.html')
def activate(template):
    form = EmailVerificationForm()
    user = current_user
    email_hash = user.generate_verification_hash()
    if form.validate_on_submit():
        if user.verify_verification_hash(form.code.data):
            user.is_verified = True
            return redirect(url_for('initialize'))
    return render_template(template, form=form, user=user, hash=email_hash)
