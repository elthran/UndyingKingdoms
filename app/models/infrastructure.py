from importlib import import_module
from random import randint, choice

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm.collections import attribute_mapped_collection

get_specifics = lambda: import_module('app.models.counties.specifics')
from lib.relationship_utils import has_many, belongs_to
from .bases import GameState, db


class Infrastructure(GameState):
    belongs_to('County', nullable=False)
    has_many(
        "Buildings",
        collection_class=attribute_mapped_collection('name'),
        cascade="all, delete, delete-orphan",
        passive_deletes=True
    )
    _cost_modifier = db.Column(db.Float)
    _fort_multiplier = db.Column(db.Float)

    @hybrid_property
    def cost_modifier(self):
        return self._cost_modifier or 0

    # noinspection PyPropertyAccess
    @cost_modifier.setter
    def cost_modifier(self, value):
        """Reduce building cost by a given percent.

        Passing in 0.2 would produce a 20% reduction in cost.
        """
        for building in self.buildings.values():
            building.gold_cost = round(
                building.gold_cost *
                (1 - value - self.cost_modifier)
            )
            building.wood_cost = round(
                building.wood_cost *
                (1 - value - self.cost_modifier)
            )
            building.stone_cost = round(
                building.stone_cost *
                (1 - value - self.cost_modifier)
            )
        self._cost_modifier = value

    @hybrid_property
    def fort_multiplier(self):
        return self._fort_multiplier or 1

    @fort_multiplier.setter
    def fort_multiplier(self, value):
        """Increase the productivity of forts.

        This is a bit of an odd one.
        fort_multiplier == 0 would make forts useless.
        fort_multiplier < 1 would reduce fort effectiveness.

        To increase for effectiveness by 20% you would do
        fort_multiplier = 1.2

        I feel that this is the most transparent and flexible way to do this
        although it follows a completely different pattern than all other effects.
        """
        fort = self.buildings['fort']
        # noinspection PyPropertyAccess
        fort.output = round(fort.output / self.fort_multiplier * value)

        self._fort_multiplier = value

    # Land
    def building_efficiencies(self):
        county = self.county
        return max(
            round(
                (county.population - self.get_workers_needed_to_be_efficient())
                / county.population, 2
            ),
            0.25
        )

    def destroy_buildings(self, land_destroyed, destroy_all=False):
        # destroy_all means it will always destroy this amount if you have it. Otherwise the amount destroyed is random.
        if destroy_all:
            destroyed = 0
        else:
            # The more available land, the less likely building are destroyed
            destroyed = randint(0, self.get_available_land())
        need_list = True
        while destroyed < land_destroyed:
            if need_list:
                building_choices = [
                    building
                    for building in self.buildings.keys()
                    if self.buildings[building].total > 0
                ]
                if len(building_choices) == 0:
                    break
                need_list = False
            this_choice = choice(building_choices)
            self.buildings[this_choice].total -= 1
            if self.buildings[this_choice].total == 0:
                need_list = True
            destroyed += 1
    # Workers / Population / Soldiers

    def get_available_land(self):
        """
        How much land you have which is empty and can be built upon.
        """
        county = self.county
        return max(county.land - sum(
            building.total + building.pending
            for building in self.buildings.values()
        ), 0)

    def get_employed_workers(self):
        """
        Returns the population who are maintaining current buildings.
        """
        return sum(
            building.workers_employed * building.total
            for building in self.buildings.values()
        )

    def get_stone_income(self):
        return self.buildings['quarry'].total * self.buildings['quarry'].output

    def get_wood_income(self):
        return self.buildings['mill'].total * self.buildings['mill'].output

    def get_workers_needed_to_be_efficient(self):
        county = self.county
        non_military_citizens = county.get_non_military_citizens()
        employed_workers = self.get_employed_workers()
        if non_military_citizens < employed_workers:
            return employed_workers - non_military_citizens
        return 0

    def produce_pending_buildings(self):
        """
        Gets a list of all buildings which can be built today. Builds it. Then recalls function.
        """
        county = self.county
        buildings_to_be_built = county.build_slots
        while buildings_to_be_built > 0:
            buildings_to_be_built -= 1
            queue = [building for building in self.buildings.values() if building.pending > 0]
            if queue:
                building = choice(queue)
                building.pending -= 1
                building.total += 1
            else:
                break

    def __init__(self, county):
        specifics = get_specifics()
        race = county.race

        self.county = county
        self.buildings = specifics.get_racial_buildings(race)
        self.cost_modifier = 0
        self.fort_multiplier = 1
