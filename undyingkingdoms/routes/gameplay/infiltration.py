from flask import render_template
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template
from sqlalchemy import desc

from undyingkingdoms import app
from undyingkingdoms.models import Infiltration
from undyingkingdoms.routes.helpers import in_active_session


@app.route('/gameplay/infiltration/', methods=['GET', 'POST'])
@mobile_template("{mobile/}gameplay/infiltration.html")
@login_required
@in_active_session
def infiltration(template):
    missions = Infiltration.query.filter_by(county_id=current_user.county.id).order_by(desc('time_created')).all()
    return render_template(template, missions=missions)
