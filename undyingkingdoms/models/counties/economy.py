from sqlalchemy.ext.hybrid import hybrid_property

from undyingkingdoms.metadata.metadata import food_produced_modifier
from undyingkingdoms.models.magic import Casting
from ..helpers import compute_modifier
from ..bases import GameState, db


class Economy(GameState):
    _grain_modifier = db.Column(db.Float)
    _grain_produced = db.Column(db.Integer)
    _dairy_modifier = db.Column(db.Float)
    _dairy_produced = db.Column(db.Integer)

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

    @grain_modifier.expression
    def grain_modifier(cls):
        # I'm not sure how to add in spells at this point ...
        return cls._grain_modifier

    @hybrid_property
    def grain_produced(self):
        county = self.county
        field = county.buildings['field']
        building_production = field.total * field.output
        # noinspection PyPropertyAccess
        return round((self._grain_produced + building_production) * self.grain_modifier)

    @grain_produced.setter
    def grain_produced(self, value):
        self._grain_produced = value

    @hybrid_property
    def dairy_modifier(self):
        county = self.county
        verdant_growth = Casting.query.filter_by(target_id=county.id, active=1, name="verdant growth").first()
        spell_effects = 0
        if verdant_growth:
            spell_effects += 0.5

        return spell_effects + self._dairy_modifier

    @dairy_modifier.setter
    def dairy_modifier(self, value):
        self._dairy_modifier = value

    @hybrid_property
    def dairy_produced(self):
        county = self.county
        building = county.buildings['pasture']
        building_production = building.total * building.output
        # noinspection PyPropertyAccess
        return round(building_production * self.dairy_modifier)

    @dairy_produced.setter
    def dairy_produced(self, value):
        self._dairy_produced = value

    def __init__(self, county):
        self.county = county
        self.grain_modifier = 1 + compute_modifier(
            food_produced_modifier, county.race, county.background
        )
        self.grain_produced = 0
        self.dairy_modifier = 1 + compute_modifier(
            food_produced_modifier, county.race, county.background
        )
        self.dairy_produced = 0
