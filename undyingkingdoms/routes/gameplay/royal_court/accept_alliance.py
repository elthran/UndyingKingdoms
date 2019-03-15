from flask import url_for
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from undyingkingdoms import app
from undyingkingdoms.models import Diplomacy


@app.route('/gameplay/accept_alliance/<int:kingdom_id>', methods=['POST'])
@login_required
def accept_alliance(kingdom_id):
    county = current_user.county
    if county.id != county.kingdom.leader:
        return redirect(url_for('overview', kingdom_id=0, county_id=0))
    alliance = Diplomacy.query.filter_by(status="Pending")\
        .filter_by(action="Alliance")\
        .filter_by(target_id=county.kingdom.id)\
        .filter_by(kingdom_id=kingdom_id)\
        .first()
    alliance.status = "In Progress"
    alliance.duration = 48
    return redirect(url_for('royal_court'))
