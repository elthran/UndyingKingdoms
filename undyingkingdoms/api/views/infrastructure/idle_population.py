from flask import jsonify, url_for
from flask.views import MethodView
from flask_login import login_required, current_user

from ...vue_safe import vue_safe_form
from undyingkingdoms.models.forms.infrastructure import ExcessProductionForm
from undyingkingdoms.static.metadata.metadata import excess_worker_choices


class IdlePopulationAPI(MethodView):
    @login_required
    def get(self):
        county = current_user.county

        excess_worker_form = ExcessProductionForm(goal=county.production_choice)
        excess_worker_form.goal.choices = excess_worker_choices

        return jsonify(
            status="success",
            message="You called on the idle workers api.",
            allocateWorkersUrl=url_for('api.infrastructure_allocate_api'),
            form=vue_safe_form(excess_worker_form),
            overworking=county.get_excess_production_value(0),
            landProduced=county.produce_land,
            reclaiming=county.get_excess_production_value(1),
            foraging=county.get_excess_production_value(2),
            relaxing=county.get_excess_production_value(3),
            goal=county.production_choice
        )
