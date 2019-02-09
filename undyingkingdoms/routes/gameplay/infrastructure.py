from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from undyingkingdoms import app
from undyingkingdoms.models import World, Transaction
from undyingkingdoms.models.forms.infrastructure import InfrastructureForm, ExcessProductionForm
from undyingkingdoms.static.metadata.metadata import all_buildings, game_descriptions


@app.route('/gameplay/infrastructure/', methods=['GET', 'POST'])
@mobile_template('{mobile/}gameplay/infrastructure.html')
@login_required
def infrastructure(template):
    if not current_user.in_active_session:
        current_user.in_active_session = True
    county = current_user.county
    world = World.query.filter_by(id=county.kingdom.world_id).first()
    
    build_form = InfrastructureForm()
    build_form.county_id.data = county.id

    if request.args.get('id') == 'build' and build_form.validate_on_submit():
        transaction = Transaction(county.id, county.county_days_in_age, world.day, "buy")
        for building in all_buildings:
            if build_form.data[building] > 0:
                county.gold -= build_form.data[building] * county.buildings[building].gold_cost
                county.wood -= build_form.data[building] * county.buildings[building].wood_cost
                county.buildings[building].pending += build_form.data[building]
                transaction.add_purchase(item_name=building,
                                         item_amount=build_form.data[building],
                                         gold_per_item=county.buildings[building].gold_cost,
                                         wood_per_item=county.buildings[building].wood_cost,
                                         iron_per_item=0)
        transaction.save()
        return redirect(url_for('infrastructure'))

    excess_worker_form = ExcessProductionForm(goal=county.production_choice)
    goal_choices = [(0, 'Produce Gold'), (1, 'Reclaim Land'), (2, 'Gather Food'), (3, 'Relax')]
    excess_worker_form.goal.choices = [(pairing[0], pairing[1]) for pairing in goal_choices]

    if request.args.get('id') == 'excess' and excess_worker_form.validate_on_submit():
        county.production_choice = excess_worker_form.goal.data
        return redirect(url_for('infrastructure'))

    return render_template(template, build_form=build_form,
                           excess_worker_form=excess_worker_form, meta_data=game_descriptions)

