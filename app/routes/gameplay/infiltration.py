from flask import render_template
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template
from sqlalchemy import desc

from app import app
from app.models.exports import Infiltration


@app.route('/gameplay/infiltration/', methods=['GET', 'POST'])
@mobile_template("{mobile/}gameplay/infiltration.html")
@login_required
def infiltration(template):
    county = current_user.county
    missions_query = Infiltration.query.filter(Infiltration.county_id==county.id, Infiltration.duration>0)
    last_mission = missions_query.order_by(desc('time_created')).first()

    missions = []
    last_mission_id = -1  # no id ever
    if last_mission:
        missions.append(last_mission)
        last_mission_id = last_mission.id
    other_missions = missions_query.filter(Infiltration.id!=last_mission_id).order_by('duration').all()
    if other_missions:
        missions += other_missions
    return render_template(
        template,
        missions=missions
    )
