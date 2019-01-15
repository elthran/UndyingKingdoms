from datetime import datetime

from flask import render_template, url_for, redirect
from flask_login import login_required, current_user
from sqlalchemy import desc

from undyingkingdoms import app
from undyingkingdoms.models import World, County, Kingdom, User, Infiltration


@app.route('/gameplay/overview/<int:kingdom_id>/<int:county_id>/', methods=['GET', 'POST'])
@login_required
def overview(kingdom_id=0, county_id=0):
    for user in User.query.filter_by(_in_active_session=True).all():
        time_since_last_activity = datetime.now() - user.time_modified
        if time_since_last_activity.total_seconds() > 300:  # A user who hasn't done anything in 5 minutes
            user.in_active_session = False
    if not current_user.in_active_session:
        current_user.in_active_session = True
    if not current_user.county:
        return redirect(url_for('initialize'))

    kingdom = Kingdom.query.filter_by(id=kingdom_id).first()
    county = County.query.filter_by(id=county_id).first()
    report = Infiltration.query.filter_by(county_id=current_user.county.id, target_id=county.id).first()
    return render_template('gameplay/overview.html', selected_kingdom=kingdom, selected_county=county, report=report)
