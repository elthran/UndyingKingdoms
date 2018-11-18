from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from undyingkingdoms import app, db
from undyingkingdoms.models.forms.economy import EconomyForm
from undyingkingdoms.static.metadata import rations_translations_tables


@login_required
@app.route('/user/achievements/', methods=['GET', 'POST'])
def achievements():
    return render_template('user/achievements.html')
