from undyingkingdoms.models.armies import Army
from undyingkingdoms.models.buildings import Building
from undyingkingdoms.models.notifications import Notification
from undyingkingdoms.models.bases import GameState, db
from random import choice, uniform, randint
from sqlalchemy.orm.collections import attribute_mapped_collection
from undyingkingdoms.static.metadata import all_buildings, all_armies


class County(GameState):
    weather_choices = ["clear skies", "stormy"]
    buildings_workers_required = {"unusable": 0, "houses": 0, "farms": 3}

    name = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    kingdom_id = db.Column(db.Integer, db.ForeignKey('kingdom.id'), nullable=False)
    total_land = db.Column(db.Integer)
    race = db.Column(db.String(32))
    tax_rate = db.Column(db.Integer)
    coffers = db.Column(db.Integer)
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
                                collection_class=attribute_mapped_collection('name'),
                                cascade="all, delete-orphan")
    armies = db.relationship("Army",
                             collection_class=attribute_mapped_collection('name'),
                             cascade="all, delete-orphan")

    def __init__(self, name, user_id, kingdom_id):

        self.name = name
        self.user_id = user_id
        self.kingdom_id = kingdom_id
        self.race = 'Dwarf'
        self.title = 'Engineer'
        self.population = 500
        self.total_land = 150
        self.hunger = 75
        self.happiness = 75
        self.tax_rate = 5
        self.coffers = 1000
        self.production = 0  # How many buildings you can build per day
        self.weather = choice(self.weather_choices)

        self.births = 0
        self.deaths = 0
        self.immigration = 0
        self.emigration = 0

        self.buildings = {name: Building(name, amount, cost, maintenance, description)
                          for name, amount, cost, maintenance, description in all_buildings}
        self.armies = {name: Army(name, amount, attack, defence, health)
                       for name, amount, attack, defence, health in all_armies}

    @property
    def available_land(self):
        """
        How much land you have which is empty and can be built upon.
        """
        built = sum(building.amount for building in self.buildings.values())
        pending = sum(building.pending for building in self.buildings.values())
        return self.total_land - built - pending

    def get_army_size(self):
        return sum(army.amount for army in self.armies.values())

    def get_unavailable_workers(self):
        """
        Returns the population who are maintaining current buildings.
        """
        return sum((building.maintenance * building.amount) for building in self.buildings.values())

    def get_available_workers(self):
        """
        Returns the population with no current duties.
        """
        return self.population - self.get_unavailable_workers() - self.get_army_size()

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

    def get_offensive_strength(self):
        strength = 0
        for unit in self.armies.values():
            strength += (unit.attack * unit.amount)
        return strength

    def get_defensive_strength(self):
        strength = 0
        for unit in self.armies.values():
            strength += (unit.defence * unit.amount)
        return strength

    def battle_results(self, enemy):
        if self.get_offensive_strength() > enemy.get_defensive_strength():
            land_gained = int(enemy.total_land * 0.1)
            self.total_land += land_gained
            enemy.total_land -= land_gained
            return "You were victorious! You gained {} acres.".format(land_gained)
        else:
            return "failure"

    def change_day(self):
        self.collect_taxes()
        self.production = self.get_production()
        self.produce_pending_buildings()
        self.update_weather()
        self.update_population()
        if self.weather == 'stormy':
            return [Notification(self.id, 'Weather Warning', 'Stormy weather has damaged your crops.')]
        return []

    def collect_taxes(self):
        self.coffers += self.population * (self.tax_rate / 100)
        self.coffers += self.production  # Any unused production is collected as income
        self.happiness = min(self.happiness + 7 - self.tax_rate, 100)

    def produce_pending_buildings(self):
        """
        Gets a list of all buildings which can be built today. Builds it. Then recalls function.
        """
        queue = [building for building in self.buildings.values()
                 if building.pending > 0 and building.cost <= self.production]
        if queue and self.production > 0:
            building = choice(queue)
            building.pending -= 1
            building.amount += 1
            self.production -= building.cost
            self.produce_pending_buildings()

    def update_weather(self):
        self.weather = choice(self.weather_choices)

    def update_population(self):
        self.deaths = self.population * uniform(0.01, 0.03)  # Deaths
        self.emigration = randint(100, 120) - self.happiness
        self.births = self.buildings['houses'].amount * 1 * self.get_population_modifier()
        self.immigration = randint(25, 75)
        self.population += (self.births + self.immigration) - (self.deaths + self.emigration)

    def get_production(self):
        return (self.get_production_modifier() * self.get_available_workers()) // 10

    def __repr__(self):
        return '<County %r (%r)>' % (self.name, self.id)
