from flask import jsonify, url_for
from flask.views import MethodView
from flask_login import login_required, current_user

from app.serializers.vue_safe import vue_safe_form
from app.models.forms.infrastructure import ExcessProductionForm
from app.metadata.metadata import excess_worker_choices, land_to_clear_ratio


class IdlePopulationAPI(MethodView):
    @login_required
    def get(self):
        county = current_user.county

        excess_worker_form = ExcessProductionForm(goal=county.production_choice)
        excess_worker_form.goal.choices = excess_worker_choices

        return jsonify(
            status="success",
            debugMessage="You called on the idle workers api.",
            allocateWorkersUrl=url_for('api.infrastructure_allocate_api'),
            form=vue_safe_form(excess_worker_form),
            overworking=county.get_excess_production_value(0),
            landProduced=county.preferences.produce_land,
            landToClear=county.land * land_to_clear_ratio,
            reclaiming=county.get_excess_production_value(1),
            foraging=county.get_excess_production_value(2),
            relaxing=county.get_excess_production_value(3),
            goal=county.production_choice
        )
