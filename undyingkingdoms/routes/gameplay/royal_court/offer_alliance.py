from flask import url_for, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from undyingkingdoms import app
from undyingkingdoms.models.exports import Kingdom, Diplomacy
from undyingkingdoms.routes.gameplay.royal_court.helpers import build_relations_form


@app.route('/gameplay/offer_alliance', methods=['POST'])
@login_required
def offer_alliance():
    county = current_user.county
    kingdom = county.kingdom
    if county.id != kingdom.leader:
        return redirect(url_for('overview'))

    relations_form = build_relations_form(kingdom)

    if relations_form.validate_on_submit():
        kingdom_id = relations_form.target_id.data
        ally = Kingdom.query.get(kingdom_id)
        alliance = Diplomacy(kingdom, ally, action=Diplomacy.ALLIANCE)
        alliance.save()
        return redirect(url_for('royal_court'))
    return jsonify(
        status='fail',
        message="Your message didn't pass form validation."
    )
