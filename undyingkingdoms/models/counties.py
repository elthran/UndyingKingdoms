from random import choice, uniform, randint

from sqlalchemy.orm.collections import attribute_mapped_collection

from undyingkingdoms.models.bases import GameState, db
from undyingkingdoms.models.notifications import Notification
from undyingkingdoms.static.metadata import dwarf_armies, human_armies, dwarf_buildings, \
    human_buildings

from copy import deepcopy


class County(GameState):
    weather_choices = ["clear skies", "stormy"]
    buildings_workers_required = {"unusable": 0, "houses": 0, "farms": 3}

    name = db.Column(db.String(128), nullable=False)
    leader = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    kingdom_id = db.Column(db.Integer, db.ForeignKey('kingdom.id'), nullable=False)
    vote = db.Column(db.Integer)

    total_land = db.Column(db.Integer)
    race = db.Column(db.String(32))
    gender = db.Column(db.String(16))
    tax = db.Column(db.Integer)
    gold = db.Column(db.Integer)
    wood = db.Column(db.Integer)
    iron = db.Column(db.Integer)
    happiness = db.Column(db.Integer)  # Out of 100
    population = db.Column(db.Integer)
    hunger = db.Column(db.Integer)  # Out of 100
    weather = db.Column(db.String(32))
    title = db.Column(db.String(32))
    production = db.Column(db.Integer)
    notifications = db.relationship('Notification', backref='kingdom')

    births = db.Column(db.Integer)
    deaths = db.Column(db.Integer)
    immigration = db.Column(db.Integer)
    emigration = db.Column(db.Integer)

    buildings = db.relationship("Building",
                                collection_class=attribute_mapped_collection('base'),
                                cascade="all, delete, delete-orphan", passive_deletes=True)
    armies = db.relationship("Army",
                             collection_class=attribute_mapped_collection('base'),
                             cascade="all, delete, delete-orphan", passive_deletes=True)

    def __init__(self, name, leader, user_id, kingdom_id, race, gender):

        self.name = name
        self.leader = leader
        self.user_id = user_id
        self.kingdom_id = kingdom_id
        self.race = race
        self.gender = gender
        self.title = 'Engineer'
        self.vote = None

        self.population = 500
        self.total_land = 150
        self.hunger = 75
        self.happiness = 75
        self.tax = 5
        self.gold = 1000
        self.wood = 100
        self.iron = 25
        self.production = 0  # How many buildings you can build per day
        self.weather = choice(self.weather_choices)

        self.births = 0
        self.deaths = 0
        self.immigration = 0
        self.emigration = 0

        if self.race == 'Dwarf':
            buildings = deepcopy(dwarf_buildings)
            armies = deepcopy(dwarf_armies)
        elif self.race == 'Human':
            buildings = deepcopy(human_buildings)
            armies = deepcopy(human_armies)
        else:
            print("UNKNOWN")

        self.buildings = buildings
        self.armies = armies

    @property
    def available_land(self):
        """
        How much land you have which is empty and can be built upon.
        """
        built = sum(building.amount for building in self.buildings.values())
        pending = sum(building.pending for building in self.buildings.values())
        return self.total_land - built - pending

    @property
    def votes(self):
        return len([county for county in self.kingdom.counties if county.vote == self.id])

    def cast_vote(self, vote):
        self.vote = vote
        self.kingdom.count_votes()

    def display_vote(self):
        if County.query.filter_by(id=self.vote).first():
            return County.query.filter_by(id=self.vote).first().name
        self.vote = self.id
        return self.name

    def get_army_size(self):
        pending = sum(army.pending for army in self.armies.values())
        ready = sum(army.amount for army in self.armies.values())
        return pending + ready

    def get_unavailable_workers(self):
        """
        Returns the population who are maintaining current buildings.
        """
        return sum((building.labour * building.amount) for building in self.buildings.values())

    def get_available_workers(self):
        """
        Returns the population with no current duties.
        """
        return max(self.population - self.get_unavailable_workers() - self.get_army_size(), 0)

    def get_production_modifier(self):
        """
        Returns the modifier for how much production each worker produces.
        """
        modifier = {'Base': 1}
        if self.race == 'Dwarf':
            modifier['Racial Bonus'] = 0.1
        if self.title == 'Engineer':
            modifier['Profession Bonus'] = 0.15
        return sum(modifier.values())

    def get_population_modifier(self):
        """
        Returns the modifier for how much production each worker produces.
        """
        modifier = {'Base': 1}
        if self.race == 'Elf':
            modifier['Racial Bonus'] = -0.1
        if self.title == 'Goblin':
            modifier['Racial Bonus'] = 0.15
        return sum(modifier.values())

    def get_offensive_strength(self, army):
        strength = 0
        for unit in self.armies.values():
            strength += army[unit.base] * unit.attack
        return strength

    def get_defensive_strength(self):
        strength = 0
        for unit in self.armies.values():
            strength += unit.amount * unit.defence
        return strength

    def get_casualties(self, army):
        casualties = 0
        for unit in self.armies.values():
            if army[unit.base] > 0:
                dead = randint(army[unit.base] // 10, army[unit.base] // 5)
                unit.amount -= dead
                casualties += dead
        return casualties

    def battle_results(self, army, enemy):
        offense = self.get_offensive_strength(army)
        defence = enemy.get_defensive_strength()
        offence_casaulties = self.get_casualties(army)
        print(offense, defence)
        if offense > defence:
            land_gained = int(enemy.total_land * 0.1)
            self.total_land += land_gained
            enemy.total_land -= land_gained
            return "You had {} power versus the enemies {} power. You were victorious! You gained {} acres but lost" \
                   " {} troops.".format(offense, defence, land_gained, offence_casaulties)
        else:
            return "You had {} power versus the enemies {} power. You failed".format(offense, defence)

    def change_day(self):
        self.collect_taxes()
        self.production = self.get_production()
        self.produce_pending_buildings()
        self.produce_pending_armies()
        self.update_weather()
        self.update_population()
        if self.weather == 'stormy':
            return [Notification(self.id, 'Weather Warning', 'Stormy weather has damaged your crops.')]
        return []

    def get_gold_income(self):
        return (self.population * (self.tax / 100)) + self.production

    def get_wood_income(self):
        mills = [building.amount for building in self.buildings.values() if building.base == 'mills']
        return sum(mills) * 1

    def get_iron_income(self):
        mines = [building.amount for building in self.buildings.values() if building.base == 'mines']
        return sum(mines) * 1

    def collect_taxes(self):
        self.gold += self.get_gold_income()
        self.wood += self.get_wood_income()
        self.iron += self.get_iron_income()
        self.happiness = min(self.happiness + 7 - self.tax, 100)

    def produce_pending_buildings(self):
        """
        Gets a list of all buildings which can be built today. Builds it. Then recalls function.
        """
        queue = [building for building in self.buildings.values()
                 if building.pending > 0
                 and building.production <= self.production
                 and building.gold <= self.gold
                 and building.wood <= self.wood]
        if queue and self.production > 0:
            building = choice(queue)
            building.pending -= 1
            building.amount += 1
            self.production -= building.production
            self.gold -= building.gold
            self.wood -= building.wood
            self.produce_pending_buildings()

    def produce_pending_armies(self):
        """
        Chooses each unit that can be produced. Chooses each one and loops through the maximum amount.
        Keeps building one until you can't or don't want to, then breaks the loop.
        """
        for unit in self.armies.values():
            for i in range(unit.training):
                if unit.pending > 0 and unit.gold <= self.gold and unit.wood <= self.wood and unit.iron <= self.iron:
                    self.gold -= unit.gold
                    self.wood -= unit.wood
                    self.iron -= unit.iron
                    unit.pending -= 1
                    unit.amount += 1
                else:
                    break

    def update_weather(self):
        self.weather = choice(self.weather_choices)

    def update_population(self):
        self.deaths = int(self.population * uniform(0.01, 0.03))  # Deaths
        self.emigration = randint(100, 125) - self.happiness
        self.births = int(self.buildings['houses'].amount * 1 * self.get_population_modifier())
        self.immigration = randint(15, 50)
        self.population += (self.births + self.immigration) - (self.deaths + self.emigration)

    def get_production(self):
        return max((self.get_production_modifier() * self.get_available_workers()) // 3, 0)

    def __repr__(self):
        return '<County %r (%r)>' % (self.name, self.id)
