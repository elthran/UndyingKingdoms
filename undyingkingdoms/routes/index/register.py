import os

from flask import url_for, redirect, render_template
from flask_login import current_user
from flask_login import login_user
from flask_mobility.decorators import mobile_template
from sendgrid import Mail, SendGridAPIClient

from undyingkingdoms import app, User
from undyingkingdoms.models.forms.register import RegisterForm


@app.route('/register/', methods=['GET', 'POST'])
@mobile_template('{mobile/}index/register.html')
def register(template):
    form = RegisterForm()
    if current_user.is_authenticated:
        return redirect(url_for('overview'))
    if form.validate_on_submit() and not User.query.filter_by(email=form.email.data).first():
        user = User(form.username.data, form.email.data, form.password.data)
        user.save()
        login_user(user)

        message = Mail(
            from_email='from_email@example.com',
            to_emails=user.email,
            subject='Welcome to Undying Kingdoms',
            html_content='<strong>You\'ll need this code to activate your account: {}</strong>'.format(
                user.generate_verification_hash()))
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e, message)

        return redirect(url_for('initialize'))
    return render_template(template, form=form)
