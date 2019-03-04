from flask import redirect, url_for, render_template, jsonify
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from undyingkingdoms import app
from undyingkingdoms.models import Kingdom, County, Notification, Diplomacy
from undyingkingdoms.models.forms.royal_court import RoyalCourtMessageForm, RoyalCourtRelationsForm


def build_relations_form(county):
    form = RoyalCourtRelationsForm()
    all_other_kingdoms = Kingdom.query.filter(Kingdom.id != county.kingdom_id).all()
    form.target_id.choices = [(kingdom.id, kingdom.name) for kingdom in all_other_kingdoms]
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

    wars = Diplomacy.query.filter_by(status="In Progress").filter_by(action="War")\
        .filter((Diplomacy.kingdom_id == county.kingdom_id) | (Diplomacy.target_id == county.kingdom_id))\
        .all()
    enemy_kingdoms = []
    for war in wars:
        enemy_kingdom = Kingdom.query.get(war.kingdom_id)
        if county.kingdom == enemy_kingdom:
            enemy_kingdom = Kingdom.query.get(war.target_id)
        enemy_kingdoms.append(enemy_kingdom)
    return render_template(template,
                           message_form=message_form,
                           relations_form=relations_form,
                           enemy_kingdoms=enemy_kingdoms)


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
        return redirect(url_for('royal_court'))
    return jsonify(
        status='fail',
        message="Your message didn't pass form validation."
    )
