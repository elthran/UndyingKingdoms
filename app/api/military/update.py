from types import SimpleNamespace

from flask import jsonify
from flask.views import MethodView
from flask_login import login_required, current_user

from .helpers import build_units, vue_safe_army
from app.metadata.metadata import game_descriptions, all_armies
from app.models.forms.military import MilitaryForm
from app.serializers.vue_safe import vue_safe_form, generic_vue_safe


class UpdateAPI(MethodView):
    @login_required
    def get(self):
        county = current_user.county
        infrastructure = county.infrastructure
        form = MilitaryForm()

        armies = county.armies
        besiegers = armies['besieger']
        lair = infrastructure.buildings['lair']

        military_strength = dict(
            offensiveStrength=county.get_offensive_strength(),
            defensiveStrength=county.get_defensive_strength(),
            availableWorkers=county.get_available_workers(),
            besiegerStrength=besiegers.total * besiegers.attack,
        )

        vue_safe_county = dict(
            population=county.population,
            gold=county.gold,
            wood=county.wood,
            iron=county.iron,
            happiness=county.happiness,
            background=county.background,
            unitsAvailable=county.get_available_army_size(),
            unitsUnavailable=county.get_unavailable_army_size(),
            unitsInTraining=county.get_training_army_size(),
            upkeepCosts=county.get_upkeep_costs(),
            **military_strength
        )

        vue_safe_armies = {
            army.key: vue_safe_army(county, army)
            for army in armies.values()
        }
        vue_safe_armies['monster']['building'] = dict(
            name=lair.class_name_plural.title(),
            total=lair.total,
        )

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
            armies=vue_safe_armies,
            armyOrdering=all_armies,
        )

    @login_required
    def post(self):
        county = current_user.county
        form = MilitaryForm()

        if form.validate(county):
            build_units(county, form)
            return jsonify(
                debugMessage='You have updated your current troop production.',
            ), 201
        return jsonify(
            debugMessage='Your troop production form did not pass validation.'
        ), 403
