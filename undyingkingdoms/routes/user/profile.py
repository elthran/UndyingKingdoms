from flask import render_template, flash
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from undyingkingdoms import app, User
from undyingkingdoms.models.forms.profile import ProfileSecurityForm, ProfileEmailForm


@app.route('/user/profile/<tab>', methods=['GET', 'POST'])
@mobile_template('{mobile/}user/profile.html')
@login_required
def profile(template, tab):
    user = current_user

    password_form = ProfileSecurityForm()
    email_form = ProfileEmailForm()

    if password_form.validate_on_submit():
        if user.check_password(password_form.old_password.data):
            user.set_password_hash(password_form.new_password.data)
            flash("You have updated your password")
        else:
            flash("Your old password was incorrect")

    elif email_form.validate_on_submit():
        existing_user = User.query.filter_by(email=email_form.email.data).first()
        if existing_user:
            flash("That email is already taken")
        else:
            if user.check_password(email_form.password.data):
                user.email = email_form.email.data
                user.is_verified = False
                flash("You have updated your email address")
            else:
                flash("Your password was incorrect")

    return render_template(template,
                           user=current_user,
                           tab=tab,
                           password_form=password_form,
                           email_form=email_form)
