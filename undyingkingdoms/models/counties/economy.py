from undyingkingdoms.metadata.metadata import food_produced_modifier
from ..helpers import compute_modifier
from ..bases import GameState, db


class Economy(GameState):
    produced_grain = db.Column(db.Integer)

    def __init__(self, county):
        self.county = county
        self.produced_grain = 1 + compute_modifier(
            food_produced_modifier, county.race, county.background
        )

    def get_produced_grain(self):
        modifier = 1
        if self.technologies['agriculture'].completed:
            modifier += self.technologies['agriculture'].output
        if self.technologies['agriculture ii'].completed:
            modifier += self.technologies['agriculture ii'].output
        modify_grain_rate = Casting.query.filter_by(target_id=self.id, name="modify_grain_rate").filter(
            (Casting.duration > 0) | (Casting.active == True)).all()
        for spell in modify_grain_rate or []:
            modifier += spell.output * self.spell_modifier
        self.produced_grain = int(self.buildings['field'].total * self.buildings['field'].output * modifier)
