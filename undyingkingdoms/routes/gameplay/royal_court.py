from flask import redirect, url_for, render_template, jsonify
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from undyingkingdoms import app
from undyingkingdoms.models import Kingdom, County, Notification, Diplomacy
from undyingkingdoms.models.forms.royal_court import RoyalCourtMessageForm, RoyalCourtRelationsForm


def build_relations_form(county):
    form = RoyalCourtRelationsForm()
    all_kingdoms = Kingdom.query.filter(Kingdom.id != county.kingdom_id).all()
    kingdoms_at_war = county.kingdom.get_enemies()
    kingdoms_at_peace = county.kingdom.get_allies() \
                        + county.kingdom.get_pending_alliance(keyword="to") \
                        + county.kingdom.get_pending_alliance(keyword="from")
    eligible_kingdoms = set(all_kingdoms) - set(kingdoms_at_war) - set(kingdoms_at_peace)
    form.target_id.choices = [(kingdom.id, kingdom.name) for kingdom in eligible_kingdoms]
    return form


@app.route('/gameplay/royal_court/', methods=['GET', 'POST'])
@mobile_template('{mobile/}gameplay/royal_court.html')
@login_required
def royal_court(template):
    county = current_user.county
    if county.id != county.kingdom.leader:
        return redirect(url_for('overview', kingdom_id=0, county_id=0))
    message_form = RoyalCourtMessageForm()

    relations_form = build_relations_form(county)

    enemy_kingdoms = county.kingdom.get_enemies()
    ally_list = county.kingdom.get_allies()
    allies = {}
    for ally in ally_list:
        allies[ally.id] = ally
    alliances = Diplomacy.query.filter_by(status="In Progress").filter_by(action="Alliance") \
            .filter((Diplomacy.kingdom_id == county.kingdom.id) | (Diplomacy.target_id == county.kingdom.id)) \
            .all()
    offers_to_us = county.kingdom.get_pending_alliance(keyword="to")
    offers_from_us = county.kingdom.get_pending_alliance(keyword="from")
    return render_template(template,
                           message_form=message_form,
                           relations_form=relations_form,
                           allies=allies,
                           enemy_kingdoms=enemy_kingdoms,
                           alliances=alliances,
                           offers_to_us=offers_to_us,
                           offers_from_us=offers_from_us)


@app.route('/gameplay/send_decree/', methods=['POST'])
@login_required
def send_decree():
    county = current_user.county
    if county.id != county.kingdom.leader:
        return redirect(url_for('overview', kingdom_id=0, county_id=0))
    message_form = RoyalCourtMessageForm()
    if message_form.validate_on_submit():
        for county in County.query.filter_by(kingdom_id=county.kingdom_id).all():
            message = Notification(
                county_id=county.id,
                title="Royal Decree from {} {}".format(county.title, county.leader),
                content=message_form.content.data,
                day=county.id,
                category="Royal Decree")
            message.save()
        return redirect(url_for('royal_court'))
    return jsonify(
        status='fail',
        message="Your message didn't pass form validation.")


@app.route('/gameplay/declare_war', methods=['POST'])
@login_required
def declare_war():
    county = current_user.county
    if county.id != county.kingdom.leader:
        return redirect(url_for('overview', kingdom_id=0, county_id=0))

    relations_form = build_relations_form(county)

    if relations_form.validate_on_submit():
        kingdom_id = relations_form.target_id.data
        enemy = Kingdom.query.get(kingdom_id)
        war = Diplomacy(county.kingdom_id, enemy.id, enemy.world.day, action="War", status="In Progress")
        war.attacker_goal = enemy.get_land_sum() // 15
        war.defender_goal = county.kingdom.get_land_sum() // 15
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


@app.route('/gameplay/offer_alliance', methods=['POST'])
@login_required
def offer_alliance():
    county = current_user.county
    if county.id != county.kingdom.leader:
        return redirect(url_for('overview', kingdom_id=0, county_id=0))

    relations_form = build_relations_form(county)

    if relations_form.validate_on_submit():
        kingdom_id = relations_form.target_id.data
        ally = Kingdom.query.get(kingdom_id)
        alliance = Diplomacy(county.kingdom_id, ally.id, ally.world.day, action="Alliance")
        alliance.save()
        return redirect(url_for('royal_court'))
    return jsonify(
        status='fail',
        message="Your message didn't pass form validation."
    )


@app.route('/gameplay/cancel_alliance/<int:kingdom_id>', methods=['POST'])
@login_required
def cancel_alliance(kingdom_id):
    county = current_user.county
    if county.id != county.kingdom.leader:
        return redirect(url_for('overview', kingdom_id=0, county_id=0))
    alliance = Diplomacy.query.filter_by(status="Pending")\
        .filter_by(action="Alliance")\
        .filter_by(kingdom_id=county.kingdom.id)\
        .filter_by(target_id=kingdom_id)\
        .first()
    alliance.status = "Cancelled"
    return redirect(url_for('royal_court'))


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
    alliance.duration = 72
    return redirect(url_for('royal_court'))


@app.route('/gameplay/decline_alliance/<int:kingdom_id>', methods=['POST'])
@login_required
def decline_alliance(kingdom_id):
    county = current_user.county
    if county.id != county.kingdom.leader:
        return redirect(url_for('overview', kingdom_id=0, county_id=0))
    alliance = Diplomacy.query.filter_by(status="Pending")\
        .filter_by(action="Alliance")\
        .filter_by(target_id=county.kingdom.id)\
        .filter_by(kingdom_id=kingdom_id)\
        .first()
    alliance.status = "Cancelled"
    return redirect(url_for('royal_court'))
