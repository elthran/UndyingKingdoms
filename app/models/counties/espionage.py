from sqlalchemy.ext.hybrid import hybrid_property

from app.metadata.metadata import amount_of_thieves_modifier, infiltration_results_modifier
from app.models.helpers import extract_modifiers
from ..bases import GameState, db


class Espionage(GameState):
    _thief_slots = db.Column(db.Integer)
    thief_slot_multiplier = db.Column(db.Integer)
    thieves_per_mission = db.Column(db.Integer)
    gain_modifier = db.Column(db.Float)
    _duration_multiplier = db.Column(db.Float)

    @hybrid_property
    def thief_slots(self):
        county = self.county
        base = county.buildings['tavern'].total
        output = county.buildings['tavern'].output
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
