from datetime import datetime, timedelta
from importlib import import_module

from sqlalchemy.ext.hybrid import hybrid_property

from lib.calculations.distributions import get_int_between_0_and_100
from app.metadata.metadata import amount_of_thieves_modifier, infiltration_results_modifier
from app.models.helpers import extract_modifiers
from ..bases import GameState, db
get_models = lambda: import_module('app.models.exports')


class Espionage(GameState):
    _thief_slots = db.Column(db.Integer)
    thief_slot_multiplier = db.Column(db.Integer)
    thieves_per_mission = db.Column(db.Integer)
    gain_modifier = db.Column(db.Float)
    _duration_multiplier = db.Column(db.Float)

    @hybrid_property
    def thief_slots(self):
        county = self.county
        infrastructure = county.infrastructure
        base = infrastructure.buildings['tavern'].total
        output = infrastructure.buildings['tavern'].output
        return base * (output + self.thief_slot_multiplier)

    @thief_slots.setter
    def thief_slots(self, value):
        self._thief_slots = value

    # noinspection PyUnresolvedReferences,PyMethodParameters
    @thief_slots.expression
    def thief_slots(cls):
        return cls._thief_slots

    @hybrid_property
    def duration_multiplier(self):
        return self._duration_multiplier or 1

    @duration_multiplier.setter
    def duration_multiplier(self, value):
        self._duration_multiplier = (value or 1)

    def get_chance_to_catch_enemy_thieves(self):
        models = get_models()
        county = self.county
        infrastructure = county.infrastructure
        buffer_time = datetime.utcnow() - timedelta(hours=12)
        operations_on_target = models.Infiltration.query.filter_by(
            target_id=county.id).filter_by(success=True).filter(
            models.Infiltration.time_created > buffer_time).all()
        chance = 0
        for mission in operations_on_target:  # Each thief who invaded you gives you some protection
            chance += (mission.amount_of_thieves * 5)

        chance += (
            (infrastructure.buildings['tower'].total ** 0.8)
            * 100 / county.land * infrastructure.buildings['tower'].output
        )

        modify_thief_prevention = models.Casting.query.filter_by(
            target_id=county.id, name="modify_thief_prevention").filter(
            (models.Casting.duration > 0) | models.Casting.active).all()
        for spell in modify_thief_prevention or []:
            chance += spell.output * county.spell_modifier

        return get_int_between_0_and_100(chance)

    def __init__(self, county):
        self.thief_slots = 0
        self.thief_slot_multiplier = 0
        self.thieves_per_mission = 1 + extract_modifiers(
            amount_of_thieves_modifier,
            county.race,
            county.background
        )
        self.gain_modifier = extract_modifiers(
            infiltration_results_modifier,
            county.race,
            county.background
        )
        self.duration_multiplier = 0
