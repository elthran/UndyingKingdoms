from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from undyingkingdoms import app, db
from undyingkingdoms.models import Infiltration, County


@app.route('/gameplay/infiltrate/<target_id>', methods=['GET', 'POST'])
@login_required
def infiltrate(target_id):
    if not current_user.logged_in:
        current_user.logged_in = True
    current_day = current_user.county.kingdom.world.day
    target = County.query.filter_by(id=target_id).first()
    report = Infiltration.query.filter_by(county_id=current_user.county.id, target_id=target_id).first()
    if not report:
        report = Infiltration(current_user.county.id, target_id, current_day, "scout")
        #db.session.add(report)
        #db.session.commit()
        report.save()
    report.get_troop_report(current_user.county, target)
    report.duration = current_user.county.get_future_thief_report_duration()
    report.day = current_day
    db.session.commit()
    return redirect(url_for('overview', kingdom_id=current_user.county.kingdom_id, county_id=target_id))
