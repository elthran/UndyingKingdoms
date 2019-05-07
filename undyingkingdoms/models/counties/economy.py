from sqlalchemy.ext.hybrid import hybrid_property

from undyingkingdoms.metadata.metadata import food_produced_modifier
from undyingkingdoms.models.magic import Casting
from ..helpers import compute_modifier, get_modifier_effects
from ..bases import GameState, db


class Economy(GameState):
    _grain_modifier = db.Column(db.Float)
    _grain_produced = db.Column(db.Integer)
    _grain_effects = db.Column(db.PickleType, default=dict(modifier={}, produced={}))

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

        self._grain_effects['modifier']['spells'] = spell_effects
        self._grain_effects['modifier']['other'] = self._grain_modifier - 1
        return self._grain_modifier + spell_effects

    @grain_modifier.setter
    def grain_modifier(self, value):
        self._grain_modifier = value

    # noinspection PyPropertyAccess
    @hybrid_property
    def grain_produced(self):
        county = self.county
        building_production = int(
            county.buildings['field'].total
            * county.buildings['field'].output
            * self.grain_modifier
        )
        self._grain_effects['produced']['buildings'] = building_production
        self._grain_effects['produced']['other'] = self._grain_produced
        return self._grain_produced + building_production

    @grain_produced.setter
    def grain_produced(self, value):
        self._grain_produced = value

    @hybrid_property
    def grain_effects(self):
        # _ = self.grain_modifier
        # _ = self.grain_produced
        return self._grain_effects

    @grain_effects.setter
    def grain_effects(self, value):
        self._grain_effects = value

    def __init__(self, county):
        self.county = county
        self.grain_modifier = 1 + compute_modifier(
            food_produced_modifier, county.race, county.background
        )
        self.grain_produced = 0
        self.grain_effects = get_modifier_effects(food_produced_modifier, county.race, county.background)
