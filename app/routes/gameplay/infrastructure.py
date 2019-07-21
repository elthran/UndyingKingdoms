from importlib import import_module

from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from app import app
from app.api.infrastructure.build_buildings import BuildBuildingsAPI
from app.api.infrastructure.helpers import max_buildable_by_cost
get_forms = lambda: import_module('app.models.forms.exports')
from app.routes.helpers import mobile_on_vue
from app.metadata.metadata import game_descriptions, excess_worker_choices, land_to_clear_ratio


@app.route('/gameplay/infrastructure/', methods=['GET'])
@mobile_on_vue
@login_required
def infrastructure():
    forms = get_forms()
    county = current_user.county

    build_form = forms.InfrastructureForm()
    build_form.county_id.data = county.id

    excess_worker_form = forms.ExcessProductionForm(goal=county.production_choice)
    excess_worker_form.goal.choices = excess_worker_choices

    return render_template(
        "gameplay/infrastructure.html",
        build_form=build_form,
        excess_worker_form=excess_worker_form,
        meta_data=game_descriptions,
        max_buildable_by_cost=max_buildable_by_cost,
        land_to_clear=county.land * land_to_clear_ratio
    )


@app.route('/gameplay/infrastructure/build/', methods=['POST'])
@login_required
def build_buildings():
    BuildBuildingsAPI().post()
    # if response.json['status'] == 'success':
    return redirect(url_for('infrastructure'))
