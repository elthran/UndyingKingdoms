from datetime import datetime
from random import randint

from flask import url_for, redirect, render_template, flash
from flask_login import current_user
from flask_login import login_user

from undyingkingdoms import app, User
from undyingkingdoms.models import Notification
from undyingkingdoms.models.forms.login import LoginForm


@app.route('/login/', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if current_user.is_authenticated:
		return redirect(
			url_for('overview', kingdom_id=current_user.county.kingdom.id, county_id=current_user.county.id))
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and user.check_password(form.password.data):
			if user.county is None:
				login_user(user)
				return redirect(url_for('initialize'))
			hours_since_last_login = (datetime.now() - user.get_last_login()).seconds // 3600
			if hours_since_last_login >= 12:
				gold_reward = max(hours_since_last_login, 48) * randint(3, 4)
				user.county.gold += gold_reward
				notification = Notification(user.county.id, "Login Reward", "Your people appreciate your trust in letting them run their own affairs. They give you {} gold as a thank you.".format(gold_reward), user.county.kingdom.world.day)
				notification.save()
			login_user(user)
			return redirect(
				url_for('overview', kingdom_id=current_user.county.kingdom.id, county_id=current_user.county.id))
		else:
			flash("Your email or password was incorrect.")
	return render_template("index/login.html", form=form, users=User.query.all())
