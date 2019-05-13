from sqlalchemy.ext.hybrid import hybrid_property

from undyingkingdoms.metadata.metadata import amount_of_thieves_modifier
from undyingkingdoms.models.helpers import compute_modifier
from ..bases import GameState, db


class Espionage(GameState):
    _thief_slots = db.Column(db.Integer)
    thief_slot_multiplier = db.Column(db.Integer)
    thieves_per_mission = db.Column(db.Integer)

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

    def __init__(self, county):
        self.thief_slots = 0
        self.thief_slot_multiplier = 0
        self.thieves_per_mission = 1 + compute_modifier(
            amount_of_thieves_modifier,
            county.race,
            county.background
        )
