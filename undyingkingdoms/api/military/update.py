from types import SimpleNamespace

from flask import jsonify
from flask.views import MethodView
from flask_login import login_required, current_user

from .helpers import build_units, vue_safe_army
from undyingkingdoms.metadata.metadata import game_descriptions, all_armies
from undyingkingdoms.models.forms.military import MilitaryForm
from undyingkingdoms.api.vue_safe import vue_safe_form, generic_vue_safe


class UpdateAPI(MethodView):
    @login_required
    def get(self):
        county = current_user.county
        form = MilitaryForm()
        form.county_id.data = county.id

        armies = county.armies
        besiegers = armies['besieger']

        military_strength = dict(
            offensiveStrength=county.get_offensive_strength(),
            defensiveStrength=county.get_defensive_strength(),
            availableWorkers=county.get_available_workers(),
            besiegerStrength=besiegers.total * besiegers.attack,
        )

        vue_safe_county = dict(
            unitsAvailable=county.get_available_army_size(),
            unitsUnavailable=county.get_unavailable_army_size(),
            unitsInTraining=county.get_training_army_size(),
            upkeepCosts=county.get_upkeep_costs(),
            **military_strength
        )

        vue_save_armies = {
            army.key: vue_safe_army(county, army)
            for army in county.armies.values()
        }

        vue_safe_metadata = generic_vue_safe(
            SimpleNamespace(id='metadata'),
            [],
            **game_descriptions
        )

        return jsonify(
            debugMessage=f"You called on {__name__}",
            form=vue_safe_form(form),
            county=vue_safe_county,
            metadata=vue_safe_metadata,
            armies=vue_save_armies,
            armyOrdering=all_armies,
        )

    @login_required
    def post(self):
        county = current_user.county
        form = MilitaryForm()

        if form.validate_on_submit():
            build_units(county, form)
            return jsonify(
                debugMessage='You have updated your current troop production.',
            ), 201
        return jsonify(
            debugMessage='Your troop production form did not pass validation.'
        ), 403
