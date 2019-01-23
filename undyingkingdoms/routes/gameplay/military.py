from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from undyingkingdoms import app
from undyingkingdoms.models import Transaction, World
from undyingkingdoms.models.forms.military import MilitaryForm
from undyingkingdoms.static.metadata import all_armies, game_descriptions


@app.route('/gameplay/military/', methods=['GET', 'POST'])
@login_required
def military():
    if not current_user.in_active_session:
        current_user.in_active_session = True
    county = current_user.county
    world = World.query.filter_by(id=county.kingdom.world_id).first()
    form = MilitaryForm()
    form.county_id.data = county.id
    if form.validate_on_submit():
        total_trained = 0
        transaction = Transaction(county.id, county.county_days_in_age, world.day, "buy")
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
        # You lose 1 happiness for each 1% of population you force into military.
        county.happiness -= (total_trained * 100 // county.population) + 1
        return redirect(url_for('military'))
    return render_template('gameplay/military.html', form=form, meta_data=game_descriptions)
