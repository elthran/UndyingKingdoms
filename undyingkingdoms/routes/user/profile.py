from flask import render_template, flash
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from undyingkingdoms import app
from undyingkingdoms.models.forms.profile import ProfileSecurityForm


@app.route('/user/profile/<tab>', methods=['GET', 'POST'])
@mobile_template('{mobile/}user/profile.html')
@login_required
def profile(template, tab):
    user = current_user
    form = ProfileSecurityForm()
    if form.validate_on_submit():
        if user.check_password(form.old_password.data):
            user.set_password_hash(form.new_password.data)
            flash("You have updated your password.")
        else:
            flash("Your old password was incorrect")
    return render_template(template, user=current_user, tab=tab, form=form)
