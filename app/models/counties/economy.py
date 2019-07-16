from math import ceil

from sqlalchemy.ext.hybrid import hybrid_property

from app.metadata.metadata import food_produced_modifier, buildings_produced_per_day, happiness_modifier, \
    income_modifier, birth_rate_modifier, production_per_worker_modifier
from app.models.magic import Casting
from ..helpers import extract_modifiers
from ..bases import GameState, db

"""
Anything that seems economic is being migrate here.
Not that some of these values have no leading underscore and
no mess of @methods. Once I fully convert the code I won't need
all the extra methods. It is just faster to do it in stages.
"""


class Economy(GameState):
    BASE_BUILD_SLOTS = 3
    BASE_HAPPINESS = 7

    _grain_modifier = db.Column(db.Float)
    _grain_produced = db.Column(db.Integer)
    _dairy_modifier = db.Column(db.Float)
    _dairy_produced = db.Column(db.Integer)
    build_slots = db.Column(db.Integer)
    happiness_change = db.Column(db.Integer)
    _iron_income = db.Column(db.Integer)
    iron_multiplier = db.Column(db.Integer)  # consider renaming to mine_multiplier
    gold_modifier = db.Column(db.Float)
    _gold_income = db.Column(db.Integer)
    _bank_income = db.Column(db.Integer)
    bank_multiplier = db.Column(db.Integer)
    _birth_rate_modifier = db.Column(db.Float)
    _birth_rate = db.Column(db.Integer)
    immigration_modifier = db.Column(db.Float)
    _immigration_rate = db.Column(db.Float)
    _excess_production = db.Column(db.Integer)
    excess_production_multiplier = db.Column(db.Float)
    production_modifier = db.Column(db.Float)

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

    # noinspection PyUnresolvedReferences,PyMethodParameters
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
        building_production *= county.building_efficiencies()
        # noinspection PyPropertyAccess
        return round((self._grain_produced + building_production) * (1 + self.grain_modifier))

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
        building_production *= county.building_efficiencies()
        # noinspection PyPropertyAccess
        return round(building_production * (1 + self.dairy_modifier))

    @dairy_produced.setter
    def dairy_produced(self, value):
        self._dairy_produced = value

    @hybrid_property
    def iron_income(self):
        county = self.county

        building_production = county.buildings['mine'].total * (county.buildings['mine'].output + self.iron_multiplier)
        building_production *= county.building_efficiencies()
        return ceil(building_production + self._iron_income)

    @iron_income.setter
    def iron_income(self, value):
        self._iron_income = value

    # noinspection PyUnresolvedReferences,PyMethodParameters
    @iron_income.expression
    def iron_income(cls):
        return cls._iron_income

    @hybrid_property
    def gold_income(self):
        county = self.county
        excess_worker_income = (
            county.get_excess_production_value()
            if county.production_choice == county.GOLD
            else 0
        )
        # noinspection PyPropertyAccess
        revenue = (self._gold_income + county.get_tax_income() + self.bank_income + excess_worker_income) * (1 + self.gold_modifier)
        expenses = county.get_upkeep_costs()
        return round(revenue - expenses)  # net income/net loss ;)

    @hybrid_property
    def bank_income(self):
        county = self.county
        building_income = county.buildings['bank'].total * (county.buildings['bank'].output + (self.bank_multiplier or 0))
        building_income *= county.building_efficiencies()
        return ceil(building_income)

    @bank_income.setter
    def bank_income(self, value):
        self._bank_income = value

    # noinspection PyMethodParameters,PyUnresolvedReferences
    @bank_income.expression
    def bank_income(cls):
        return cls._bank_income

    @gold_income.setter
    def gold_income(self, value):
        self._gold_income = value

    # noinspection PyUnresolvedReferences,PyMethodParameters
    @gold_income.expression
    def gold_income(cls):
        return cls._gold_income

    @hybrid_property
    def birth_rate_modifier(self):
        county = self.county
        modifier = self._birth_rate_modifier
        modifier += (county.buildings['house'].total ** 0.75) / county.land * county.buildings['house'].output
        modify_birth_rate = Casting.query.filter_by(target_id=county.id, name="modify_birth_rate").filter(
            (Casting.duration > 0) | Casting.active).all()
        for spell in modify_birth_rate or []:
            modifier += spell.output * county.spell_modifier
        return modifier

    @hybrid_property
    def get_ration_modifier(self):
        hungry_people = self.get_food_to_be_eaten() - self.grain_stores - self.get_produced_dairy() - self.get_produced_grain()

        if hungry_people <= 0:  # You fed everyone
            if self.rations == 0:
                return -6
            elif self.rations < 1:
                return int(- 1 / self.rations - 1)
            else:
                return int(self.rations * 2)
        else:  # You can't feed everyone
            return -((hungry_people // 200) + 1)

    @hybrid_property
    def get_noxious_fumes_modifier(self):
        noxious_fumes = Casting.query.filter_by(target_id=self.id, name="noxious_fumes").filter(
            (Casting.duration > 0) | (Casting.active == True)).all()
        if noxious_fumes:
            return -3

    @birth_rate_modifier.setter
    def birth_rate_modifier(self, value):
        self._birth_rate_modifier = value

    # noinspection PyUnresolvedReferences,PyMethodParameters
    @birth_rate_modifier.expression
    def birth_rate_modifier(cls):
        return cls._birth_rate_modifier

    @hybrid_property
    def birth_rate(self):
        county = self.county
        raw_rate = (county.happiness / 100) * (county.land / 5)  # 5% times your happiness rating
        # noinspection PyPropertyAccess
        return round(raw_rate * (1 + self.birth_rate_modifier))

    @birth_rate.setter
    def birth_rate(self, value):
        self._birth_rate = value

    # noinspection PyUnresolvedReferences,PyMethodParameters
    @birth_rate.expression
    def birth_rate(cls):
        return cls._birth_rate

    @hybrid_property
    def immigration_rate(self):
        county = self.county
        kingdom = county.kingdom
        world = kingdom.world
        rate = (self._immigration_rate or 0)
        modifier = 1 + (self.immigration_modifier or 0)
        random_hash = (world.day ** 2) % 10
        return (25 + random_hash + rate) * modifier

    @immigration_rate.setter
    def immigration_rate(self, value):
        self._immigration_rate = value

    # noinspection PyUnresolvedReferences,PyMethodParameters
    @immigration_rate.expression
    def immigration_rate(cls):
        return cls._immigration_rate

    @hybrid_property
    def excess_production(self):
        """
        Returns the amount of excess production you get each turn
        """
        county = self.county
        return max(round(
            county.get_available_workers() *
            (1 + self.production_modifier) *
            self.excess_production_multiplier
        ), 0)

    @excess_production.setter
    def excess_production(self, value):
        self._excess_production = value

    # noinspection PyUnresolvedReferences,PyMethodParameters
    @excess_production.expression
    def excess_production(cls):
        return cls._excess_production

    def __init__(self, county):
        self.county = county
        self.grain_modifier = extract_modifiers(
            food_produced_modifier, county.race, county.background
        )
        self.grain_produced = 0
        self.dairy_modifier = extract_modifiers(
            food_produced_modifier, county.race, county.background
        )
        self.dairy_produced = 0
        self.build_slots = self.BASE_BUILD_SLOTS + extract_modifiers(
            buildings_produced_per_day, county.race, county.background
        )
        self.happiness_change = self.BASE_HAPPINESS + extract_modifiers(
            happiness_modifier, county.race, county.background
        )
        self.iron_income = 0
        self.iron_multiplier = 0
        self.gold_modifier = extract_modifiers(income_modifier, county.race, county.background)
        self.gold_income = 0
        self.bank_multiplier = 0
        self.birth_rate_modifier = extract_modifiers(birth_rate_modifier, county.race, county.background)
        self.birth_rate = 0
        self.immigration_modifier = 0
        self.immigration_rate = 0
        self.excess_production = 0
        self.excess_production_multiplier = 1
        self.production_modifier = extract_modifiers(production_per_worker_modifier, county.race, county.background)
