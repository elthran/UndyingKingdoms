from flask import url_for
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from app import app
from app.models.exports import Diplomacy


@app.route('/gameplay/accept_alliance/<int:kingdom_id>', methods=['POST'])
@login_required
def accept_alliance(kingdom_id):
    county = current_user.county
    if county.id != county.kingdom.leader:
        return redirect(url_for('overview'))
    alliance = Diplomacy.query.filter_by(status=Diplomacy.PENDING)\
        .filter_by(action=Diplomacy.ALLIANCE)\
        .filter_by(target_id=county.kingdom.id)\
        .filter_by(kingdom_id=kingdom_id)\
        .first()
    alliance.status = Diplomacy.IN_PROGRESS
    alliance.duration = 48
    return redirect(url_for('royal_court'))
