from importlib import import_module

from flask import url_for
from flask_login import current_user, login_required

from app.serializers.vue_safe import vue_safe_form
from app.metadata.metadata import excess_worker_choices, land_to_clear_ratio
from lib.base_controller import CRUDMethodView
get_forms = lambda: import_module('app.models.forms.infrastructure')


class InfrastructureController(CRUDMethodView):
    def __init__(self):
        # TODO: work out how to reuse these for the same user.
        forms = get_forms()
        county = current_user.county
        self.excess_worker_form = forms.ExcessProductionForm(
            goal=county.production_choice
        )
        self.excess_worker_form.goal.choices = excess_worker_choices
        self.county = county
        self.infrastructure = county.infrastructure

    @login_required
    def read(self):
        county = self.county
        infrastructure = self.infrastructure

        # TODO: move this code into an InfrastructureSerializer class.
        # after I fix my controller_utils implementation.
        # CONSIDER: moving all county code to a county controller?
        return dict(
            allocate_workers_url=url_for('api.infrastructure_controller_update'),
            citizens=county.population,
            citizens_available=county.get_available_workers(),
            citizens_needed=infrastructure.get_workers_needed_to_be_efficient(),
            efficiency=infrastructure.building_efficiencies(),
            foraging=county.get_excess_production_value(2),
            goal=county.production_choice,
            form=vue_safe_form(self.excess_worker_form),
            land=county.land,
            land_available=infrastructure.get_available_land(),
            land_produced=county.preferences.produce_land,
            land_to_clear=county.land * land_to_clear_ratio,
            overworking=county.get_excess_production_value(0),
            reclaiming=county.get_excess_production_value(1),
            relaxing=county.get_excess_production_value(3),
        ), 200

    @login_required
    def allocate(self):
        county = self.county
        goal = self.excess_worker_form.goal

        if self.excess_worker_form.validate_on_submit():
            county.production_choice = goal.data
            production_choice = goal.choices[county.production_choice]
            return dict(
                # **infrastructure
                # I think this should probably return the original
                # infrastructure object? or all the data in the
                # read method?
                debug_message=f"You allocated workers to {production_choice}"
            ), 200
        return dict(
            error="Your allocation form failed to pass validation."
        ), 400
