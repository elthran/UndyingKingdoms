from flask import render_template
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template
from sqlalchemy import desc

from undyingkingdoms import app
from undyingkingdoms.models import Infiltration


@app.route('/gameplay/research/', methods=['GET', 'POST'])
@mobile_template("{mobile/}gameplay/research.html")
@login_required
def research(template):
    missions = Infiltration.query.filter_by(county_id=current_user.county.id).order_by(desc('time_created')).all()
    return render_template(template, missions=missions)
