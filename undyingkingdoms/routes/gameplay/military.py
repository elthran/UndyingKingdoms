from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from undyingkingdoms import app
from undyingkingdoms.models import Transaction, World
from undyingkingdoms.models.forms.military import MilitaryForm
from undyingkingdoms.static.metadata.metadata import all_armies, game_descriptions


def monsters_buildable(county):
    return county.buildings['lair'].total - \
            county.armies['monster'].total - \
            county.armies['monster'].currently_training


def max_trainable_by_cost(county, army):
    max_size = min(
        county.gold // army.gold,
        county.wood // army.wood,
        county.iron // army.iron
    )
    if army.base_name == 'monster':
        return min(
            max_size,
            monsters_buildable(county)
        )
    return max_size


@app.route('/gameplay/military/', methods=['GET', 'POST'])
@mobile_template('{mobile/}gameplay/military.html')
@login_required
def military(template):
    county = current_user.county
    world = World.query.filter_by(id=county.kingdom.world_id).first()
    form = MilitaryForm()
    form.county_id.data = county.id
    if form.validate_on_submit():
        total_trained = 0
        transaction = Transaction(county.id, county.county_age, world.day, "buy")
        for army in all_armies:
            if form.data[army] > 0:
                total_trained += form.data[army]
                county.gold -= form.data[army] * county.armies[army].gold
                county.wood -= form.data[army] * county.armies[army].wood
                county.iron -= form.data[army] * county.armies[army].iron
                county.armies[army].currently_training += form.data[army]
                transaction.add_purchase(item_name=army,
                                         item_amount=form.data[army],
                                         gold_per_item=county.armies[army].gold,
                                         wood_per_item=county.armies[army].wood,
                                         iron_per_item=county.armies[army].iron)
        transaction.save()
        if county.background == 'Warlord':
            happiness_penalty = 0
        else:
            # You lose 1 happiness for each 0.5% of population you force into military.
            happiness_penalty = (total_trained * 200 // county.population) + 1
        county.happiness -= happiness_penalty
        return redirect(url_for('military'))

    return render_template(
        template, form=form,
        meta_data=game_descriptions,
        max_trainable_by_cost=max_trainable_by_cost,
        monsters_buildable=monsters_buildable)
