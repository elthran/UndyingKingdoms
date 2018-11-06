from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from undyingkingdoms import app, db
from undyingkingdoms.models.forms.infrastructure import InfrastructureForm
from undyingkingdoms.static.metadata import all_buildings


@login_required
@app.route('/gameplay/kingdom/', methods=['GET', 'POST'])
def kingdom():
    return render_template('gameplay/kingdom.html')
