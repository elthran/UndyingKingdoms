from flask import render_template
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template
from sqlalchemy import desc

from undyingkingdoms import app
from undyingkingdoms.models import Infiltration
from undyingkingdoms.models.trades import Trade


@app.route('/gameplay/diplomacy/', methods=['GET', 'POST'])
@mobile_template("{mobile/}gameplay/diplomacy.html")
@login_required
def diplomacy(template):
    if not current_user.in_active_session:
        current_user.in_active_session = True
    county = current_user.county
    trades_offered = Trade.query.filter_by(county_id=county.id).all()
    trades_received = Trade.query.filter_by(target_id=county.id).all()
    return render_template(template, trades_offered=trades_offered, trades_received=trades_received)
