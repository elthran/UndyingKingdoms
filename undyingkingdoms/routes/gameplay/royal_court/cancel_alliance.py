from flask import url_for
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from undyingkingdoms import app
from undyingkingdoms.models.exports import Diplomacy


@app.route('/gameplay/cancel_alliance/<int:kingdom_id>', methods=['POST'])
@login_required
def cancel_alliance(kingdom_id):
    county = current_user.county
    if county.id != county.kingdom.leader:
        return redirect(url_for('overview'))
    alliance = Diplomacy.query.filter_by(status="Pending")\
        .filter_by(action="Alliance")\
        .filter_by(kingdom_id=county.kingdom.id)\
        .filter_by(target_id=kingdom_id)\
        .first()
    alliance.status = "Cancelled"
    return redirect(url_for('royal_court'))
