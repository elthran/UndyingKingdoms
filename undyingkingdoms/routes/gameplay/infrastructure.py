from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from undyingkingdoms import app
from undyingkingdoms.blueprints.api.views.infrastructure.build_buildings import BuildBuildingsAPI
from undyingkingdoms.blueprints.api.views.infrastructure.helpers import max_buildable_by_cost
from undyingkingdoms.models.forms.infrastructure import InfrastructureForm, ExcessProductionForm
from undyingkingdoms.routes.helpers import mobile_on_vue
from undyingkingdoms.static.metadata.metadata import game_descriptions, excess_worker_choices


@app.route('/gameplay/infrastructure/', methods=['GET'])
@mobile_on_vue
@login_required
def infrastructure():
    county = current_user.county

    build_form = InfrastructureForm()
    build_form.county_id.data = county.id

    excess_worker_form = ExcessProductionForm(goal=county.production_choice)
    excess_worker_form.goal.choices = excess_worker_choices

    return render_template(
        "gameplay/infrastructure.html",
        build_form=build_form,
        excess_worker_form=excess_worker_form,
        meta_data=game_descriptions,
        max_buildable_by_cost=max_buildable_by_cost
    )


@app.route('/gameplay/infrastructure/build/', methods=['POST'])
@login_required
def build_buildings():
    BuildBuildingsAPI().post()
    # if response.json['status'] == 'success':
    return redirect(url_for('infrastructure'))
