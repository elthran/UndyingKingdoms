from undyingkingdoms.models.notifications import Notification
from undyingkingdoms.models.bases import GameState, db
from random import choice
from sqlalchemy.orm.collections import attribute_mapped_collection

from undyingkingdoms.static.metadata import all_buildings


class Building(GameState):
    county_id = db.Column(db.Integer,
                          db.ForeignKey('county.id', ondelete="CASCADE"), nullable=False, )
    name = db.Column(db.String(64))
    amount = db.Column(db.Integer)
    pending = db.Column(db.Integer)

    def __init__(self, name):
        self.name = name
        self.amount = 10
        self.pending = 0


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

    buildings = db.relationship("Building",
                                collection_class=attribute_mapped_collection('name'),
                                cascade="all, delete-orphan")

    archers = db.Column(db.Integer)
    footmen = db.Column(db.Integer)

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

        self.buildings = {name: Building(name) for name in all_buildings}

        self.archers = 50
        self.footmen = 5

    @property
    def production_cost(self):
        """
        How much production each building will cost.
        """
        return 20

    @property
    def available_land(self):
        """
        How much land you have which is empty and can be built upon.
        """
        amount = sum([building.amount for building in self.buildings.values()])
        return self.total_land - amount

    def get_army_size(self):
        return sum([self.archers, self.footmen])

    def queue_buildings(self):
        """
        Adds buildings to the list of things waiting to be built.
        Returns True if the request is possible.
        """
        return True

    def get_maintenance_workers(self):
        """
        Returns the number of workers currently required to keep all buildings running properly.
        """
        workers_required = 0
        return workers_required

    def get_production_modifier(self):
        """
        Returns the modifier for how much production each worker produces.
        """
        modifier = {'Base': 0}
        if self.race == 'Dwarf':
            modifier['Racial Bonus'] = 0.1
        if self.title == 'Engineer':
            modifier['Profession Bonus'] = 0.15
        return sum(modifier.values())

    def change_day(self):
        self.collect_taxes()
        self.refresh_production()
        self.produce_buildings_in_queue()
        self.update_weather()
        self.update_population()
        if self.weather == 'stormy':
            return [Notification(self.id, 'Weather Warning', 'Stormy weather has damaged your crops.')]
        return []

    def collect_taxes(self):
        self.coffers += self.population * (self.tax_rate / 100)
        self.happiness += (7 - self.tax_rate)

    def produce_buildings_in_queue(self):
        queue = [building for building in self.buildings.values() if building.pending > 0]
        if queue and self.production > 0:
            building = choice(queue)
            building.pending -= 1
            building.amount += 1
            self.production -= 1
            self.produce_buildings_in_queue()

    def update_weather(self):
        self.weather = choice(self.weather_choices)

    def update_population(self):
        self.population = self.population * 0.95  # Deaths

    def refresh_production(self):
        # base_production_per_worker = 1 + self.get_production_modifier()
        # number_of_workers_available = (self.population - self.get_maintenance_workers() - self.get_army_size()) / 60
        self.production = 5

    def __repr__(self):
        return '<County %r (%r)>' % (self.name, self.id)
