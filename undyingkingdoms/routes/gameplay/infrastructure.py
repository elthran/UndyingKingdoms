from flask import render_template, redirect, url_for, send_from_directory, jsonify
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from undyingkingdoms import app
from undyingkingdoms.blueprints.api.views.infrastructure.helpers import max_buildable_by_cost
from undyingkingdoms.models import World, Transaction
from undyingkingdoms.models.forms.infrastructure import InfrastructureForm, ExcessProductionForm
from undyingkingdoms.static.metadata.metadata import all_buildings, game_descriptions, excess_worker_choices


@app.route('/gameplay/infrastructure/', methods=['GET'])
@mobile_template('{mobile/}gameplay/infrastructure.html')
@login_required
def infrastructure(template):
    if 'mobile' in template:
        return send_from_directory('static/dist', 'infrastructure.html')

    county = current_user.county

    build_form = InfrastructureForm()
    build_form.county_id.data = county.id

    excess_worker_form = ExcessProductionForm(goal=county.production_choice)
    excess_worker_form.goal.choices = excess_worker_choices

    return render_template(
        template,
        build_form=build_form,
        excess_worker_form=excess_worker_form,
        meta_data=game_descriptions,
        max_buildable_by_cost=max_buildable_by_cost
    )


@app.route('/gameplay/infrastructure/build/', methods=['POST'])
@login_required
def build_buildings():
    county = current_user.county
    world = World.query.get(county.kingdom.world_id)

    build_form = InfrastructureForm()
    build_form.county_id.data = county.id

    if build_form.validate_on_submit():
        transaction = Transaction(county.id, county.day, world.day, "buy")
        for building in all_buildings:
            if build_form.data[building] > 0:
                county.gold -= build_form.data[building] * county.buildings[building].gold_cost
                county.wood -= build_form.data[building] * county.buildings[building].wood_cost
                county.stone -= build_form.data[building] * county.buildings[building].stone_cost
                county.buildings[building].pending += build_form.data[building]
                transaction.add_purchase(item_name=building,
                                         item_amount=build_form.data[building],
                                         gold_per_item=county.buildings[building].gold_cost,
                                         wood_per_item=county.buildings[building].wood_cost,
                                         stone_per_item=county.buildings[building].stone_cost)
        transaction.save()
    return redirect(url_for('infrastructure'))


@app.route('/gameplay/infrastructure/allocate/', methods=['POST'])
@login_required
def allocate_workers():
    county = current_user.county
    excess_worker_form = ExcessProductionForm(goal=county.production_choice)
    excess_worker_form.goal.choices = excess_worker_choices

    if excess_worker_form.validate_on_submit():
        county.production_choice = excess_worker_form.goal.data
        return jsonify(
            status="success",
            message="You allocated workers to ..."
        )
    return jsonify(
        status="fail",
        message="Your allocation form failed to pass validation."
    )
