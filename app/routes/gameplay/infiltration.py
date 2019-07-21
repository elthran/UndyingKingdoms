from importlib import import_module

from flask import render_template
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template
from sqlalchemy import desc

from app import app
get_models = lambda: import_module('app.models.exports')


@app.route('/gameplay/infiltration/', methods=['GET', 'POST'])
@mobile_template("{mobile/}gameplay/infiltration.html")
@login_required
def infiltration(template):
    models = get_models()
    county = current_user.county
    espionage = county.espionage
    missions_query = models.Infiltration.query.filter(
        models.Infiltration.county_id == county.id,
        models.Infiltration.duration > 0
    )
    last_mission = missions_query.order_by(desc('time_created')).first()

    missions = []
    last_mission_id = -1  # no id ever
    if last_mission:
        missions.append(last_mission)
        last_mission_id = last_mission.id
    other_missions = missions_query.filter(
        models.Infiltration.id != last_mission_id
    ).order_by('duration').all()
    if other_missions:
        missions += other_missions
    return render_template(
        template,
        missions=missions,
        espionage=espionage,
    )
