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
    leader = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    kingdom_id = db.Column(db.Integer, db.ForeignKey('kingdom.id'), nullable=False)
    total_land = db.Column(db.Integer)
    race = db.Column(db.String(32))
    tax_rate = db.Column(db.Integer)
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
                                collection_class=attribute_mapped_collection('name'),
                                cascade="all, delete, delete-orphan", passive_deletes=True)
    armies = db.relationship("Army",
                             collection_class=attribute_mapped_collection('base'),
                             cascade="all, delete, delete-orphan", passive_deletes=True)

    def __init__(self, name, leader, user_id, kingdom_id, race):

        self.name = name
        self.leader = leader
        self.user_id = user_id
        self.kingdom_id = kingdom_id
        self.race = race
        self.title = 'Engineer'
        self.population = 500
        self.total_land = 150
        self.hunger = 75
        self.happiness = 75
        self.tax_rate = 5
        self.gold = 1000
        self.wood = 100
        self.iron = 25
        self.production = 0  # How many buildings you can build per day
        self.weather = choice(self.weather_choices)

        self.births = 0
        self.deaths = 0
        self.immigration = 0
        self.emigration = 0

        self.buildings = {name: Building(name, amount, cost, maintenance, description)
                          for name, amount, cost, maintenance, description in all_buildings}

        if self.race == 'Dwarf':
            self.armies = {'peasant': Army(base='peasant',
                                           name='miners',
                                           amount=100,
                                           training=25,
                                           gold=1,
                                           iron=1,
                                           wood=1,
                                           attack=2,
                                           defence=1,
                                           health=2,
                                           description='Miners deal extra damage.'),
                           'soldier': Army(base='soldier',
                                           name='axemen',
                                           amount=15,
                                           training=10,
                                           gold=3,
                                           iron=1,
                                           wood=1,
                                           attack=2,
                                           defence=2,
                                           health=3,
                                           description='Axemen are well-rounded soldiers.'),
                           'archer': Army(base='archer',
                                          name='crossbowmen',
                                          amount=15,
                                          training=15,
                                          gold=3,
                                          iron=1,
                                          wood=1,
                                          attack=1,
                                          defence=3,
                                          health=3,
                                          description='Crossbowmen can be trained more quickly than other archers.'),
                           'elite': Army(base='elite',
                                         name='greybeards',
                                         amount=0,
                                         training=5,
                                         gold=10,
                                         iron=2,
                                         wood=1,
                                         attack=6,
                                         defence=5,
                                         health=5,
                                         description='Greybeards are capable of defending, as well as attacking.')
                           }
        elif self.race == 'Human':
            self.armies = {'peasant': Army(base='peasant',
                                           name='men-at-arms',
                                           amount=100,
                                           training=50,
                                           gold=1,
                                           iron=0,
                                           wood=1,
                                           attack=1,
                                           defence=1,
                                           health=1,
                                           description='Men-at-arms can be trained extremely quickly.'),
                           'soldier': Army(base='soldier',
                                           name='footmen',
                                           amount=15,
                                           training=10,
                                           gold=4,
                                           iron=2,
                                           wood=0,
                                           attack=3,
                                           defence=2,
                                           health=2,
                                           description='Footmen are strong attackers.'),
                           'archer': Army(base='archer',
                                          name='bowmen',
                                          amount=15,
                                          training=10,
                                          gold=2,
                                          iron=0,
                                          wood=3,
                                          attack=1,
                                          defence=3,
                                          health=2,
                                          description='Bowmen are great at defending.'),
                           'elite': Army(base='elite',
                                         name='knights',
                                         amount=0,
                                         training=5,
                                         gold=15,
                                         iron=5,
                                         wood=1,
                                         attack=8,
                                         defence=3,
                                         health=7,
                                         description='Knights are one of the best attackers.')
                           }

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

    def battle_results(self, army, enemy):
        offense = self.get_offensive_strength(army)
        defence = enemy.get_defensive_strength()
        print(offense, defence)
        if offense > defence:
            land_gained = int(enemy.total_land * 0.1)
            self.total_land += land_gained
            enemy.total_land -= land_gained
            return "You had {} power versus the enemies {} power. You were victorious! You gained {} acres.".format(
                offense, defence, land_gained)
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

    def collect_taxes(self):
        self.gold += self.population * (self.tax_rate / 100)
        self.gold += self.production  # Any unused production is collected as income
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
        self.deaths = self.population * uniform(0.01, 0.03)  # Deaths
        self.emigration = randint(100, 120) - self.happiness
        self.births = self.buildings['houses'].amount * 1 * self.get_population_modifier()
        self.immigration = randint(25, 75)
        self.population += (self.births + self.immigration) - (self.deaths + self.emigration)

    def get_production(self):
        return (self.get_production_modifier() * self.get_available_workers()) // 10

    def __repr__(self):
        return '<County %r (%r)>' % (self.name, self.id)
