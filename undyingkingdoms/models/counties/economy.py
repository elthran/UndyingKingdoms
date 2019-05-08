from sqlalchemy.ext.hybrid import hybrid_property

from undyingkingdoms.metadata.metadata import food_produced_modifier
from undyingkingdoms.models.magic import Casting
from ..helpers import compute_modifier
from ..bases import GameState, db


class Economy(GameState):
    _grain_modifier = db.Column(db.Float)
    _grain_produced = db.Column(db.Integer)

    @hybrid_property
    def grain_modifier(self):
        county = self.county
        grain_modifier_spells = Casting.query.filter_by(
            target_id=county.id, name="modify_grain_rate"
        ).filter(
            (Casting.duration > 0) | Casting.active
        ).all()
        spell_effects = 0
        for spell in grain_modifier_spells:
            spell_effects += spell.output * county.spell_modifier

        return self._grain_modifier + spell_effects

    @grain_modifier.setter
    def grain_modifier(self, value):
        self._grain_modifier = value

    # noinspection PyPropertyAccess
    @hybrid_property
    def grain_produced(self):
        county = self.county
        field = county.buildings['field']
        building_production = field.total * field.output
        return round((self._grain_produced + building_production) * self.grain_modifier)

    @grain_produced.setter
    def grain_produced(self, value):
        self._grain_produced = value

    def __init__(self, county):
        self.county = county
        self.grain_modifier = 1 + compute_modifier(
            food_produced_modifier, county.race, county.background
        )
        self.grain_produced = 0
