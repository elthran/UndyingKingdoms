from flask import url_for, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from undyingkingdoms import app
from undyingkingdoms.models import Kingdom, Diplomacy, Notification
from undyingkingdoms.routes.gameplay.royal_court.helpers import build_relations_form


@app.route('/gameplay/declare_war', methods=['POST'])
@login_required
def declare_war():
    county = current_user.county
    if county.id != county.kingdom.leader:
        return redirect(url_for('overview', kingdom_id=0, county_id=0))

    relations_form = build_relations_form(county.kingdom)

    if relations_form.validate_on_submit():
        kingdom_id = relations_form.target_id.data
        enemy = Kingdom.query.get(kingdom_id)
        war = Diplomacy(county.kingdom_id, enemy.id, enemy.world.day, action="War", status="In Progress")
        war.attacker_goal = county.kingdom.get_land_sum() // 10
        war.defender_goal = enemy.get_land_sum() // 10
        war.save()
        pending_alliance = Diplomacy.query.filter_by(status="Pending").filter_by(action="Alliance") \
            .filter((Diplomacy.kingdom_id == county.kingdom.id) | (Diplomacy.target_id == county.kingdom.id)) \
            .filter((Diplomacy.kingdom_id == enemy.id) | (Diplomacy.target_id == enemy.id)) \
            .first()
        if pending_alliance:
            pending_alliance.status = "Cancelled"

        for enemy_county in enemy.counties:
            notice = Notification(enemy_county.id, "War", "{} has declared war on you".format(county.kingdom.name), enemy.world.day, "War")
            notice.save()
        for friendly_county in county.kingdom.counties:
            notice = Notification(friendly_county.id, "War", "We have declared war on {}".format(enemy.name),
                                  enemy.world.day, "War")
            notice.save()
        return redirect(url_for('royal_court'))
    return jsonify(
        status='fail',
        message="Your message didn't pass form validation."
    )
