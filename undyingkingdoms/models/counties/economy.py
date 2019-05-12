from sqlalchemy.ext.hybrid import hybrid_property

from undyingkingdoms.metadata.metadata import food_produced_modifier, buildings_produced_per_day, happiness_modifier, \
    income_modifier
from undyingkingdoms.models.magic import Casting
from ..helpers import compute_modifier
from ..bases import GameState, db


class Economy(GameState):
    _grain_modifier = db.Column(db.Float)
    _grain_produced = db.Column(db.Integer)
    _dairy_modifier = db.Column(db.Float)
    _dairy_produced = db.Column(db.Integer)
    build_slots = db.Column(db.Integer)
    happiness_change = db.Column(db.Integer)
    _iron_income = db.Column(db.Integer)
    iron_multiplier = db.Column(db.Integer)
    gold_modifier = db.Column(db.Float)
    _gold_income = db.Column(db.Integer)

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
        UserWarning("This function hasn't been implemented yet.")
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

    @hybrid_property
    def iron_income(self):
        county = self.county

        building_production = county.buildings['mine'].total * (county.buildings['mine'].output + self.iron_multiplier)
        return building_production + self._iron_income

    @iron_income.setter
    def iron_income(self, value):
        self._iron_income = value

    @iron_income.expression
    def iron_income(self):
        return self._iron_income

    @hybrid_property
    def gold_income(self):
        county = self.county
        excess_worker_income = (
            county.get_excess_production_value()
            if county.production_choice == county.GOLD
            else 0
        )
        revenue = self._gold_income
        revenue += (county.get_tax_income() + county.get_bank_income() + excess_worker_income) * self.gold_modifier
        expenses = county.get_upkeep_costs()
        return round(revenue - expenses)  # net income/net loss ;)

    @gold_income.setter
    def gold_income(self, value):
        self._gold_income = value

    @gold_income.expression
    def gold_income(self):
        return self._gold_income

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
        self.build_slots = 3 + compute_modifier(buildings_produced_per_day, county.race, county.background)
        self.happiness_change = 7 + compute_modifier(happiness_modifier, county.race, county.background)
        self.iron_income = 0
        self.iron_multiplier = 0
        self.gold_modifier = 1 + compute_modifier(income_modifier, county.race, county.background)
        self.gold_income = 0
