from flask import render_template
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template
from sqlalchemy import desc

from undyingkingdoms import app
from undyingkingdoms.models import Infiltration


@app.route('/gameplay/infiltration/', methods=['GET', 'POST'])
@mobile_template("{mobile/}gameplay/infiltration.html")
@login_required
def infiltration(template):
    county = current_user.county
    missions_query = Infiltration.query.filter(Infiltration.county_id==county.id, Infiltration.duration>0)
    last_mission = missions_query.order_by(desc('time_created')).first()
    last_mission_id = last_mission.id if last_mission else -1  # no id ever
    missions = missions_query.filter(Infiltration.id!=last_mission_id).order_by('duration').all()
    return render_template(
        template,
        missions=[last_mission] + missions
    )
