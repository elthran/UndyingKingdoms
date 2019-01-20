from flask import render_template
from flask_login import login_required, current_user

from undyingkingdoms import app
from undyingkingdoms.models import Infiltration


@app.route('/gameplay/infiltration/', methods=['GET', 'POST'])
@login_required
def infiltration():
    if not current_user.in_active_session:
        current_user.in_active_session = True
    missions = Infiltration.query.filter_by(county_id=current_user.county.id).all()
    return render_template('gameplay/infiltration.html', missions=missions)
