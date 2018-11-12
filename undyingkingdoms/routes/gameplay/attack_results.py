from flask import render_template, url_for, redirect
from flask_login import login_required, current_user

from undyingkingdoms import app, db
from undyingkingdoms.models import County
from undyingkingdoms.models.forms.attack import AttackForm
from undyingkingdoms.static.metadata import all_armies


@login_required
@app.route('/gameplay/attack_results/', methods=['GET', 'POST'])
def attack_results():
    return render_template('gameplay/attack_results.html', results=results)
