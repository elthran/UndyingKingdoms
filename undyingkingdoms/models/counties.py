from datetime import datetime, timedelta
from random import choice, uniform, randint, seed

from sqlalchemy.orm.collections import attribute_mapped_collection

from undyingkingdoms.models.bases import GameState, db
from undyingkingdoms.models.notifications import Notification
from undyingkingdoms.models.expeditions import Expedition
from undyingkingdoms.models.infiltrations import Infiltration
from undyingkingdoms.static.metadata import dwarf_armies, human_armies, dwarf_buildings, \
    human_buildings, kingdom_names

from copy import deepcopy


class County(GameState):
    weather_choices = ["clear skies", "stormy", "sunny", "cloudy", "light rain", "overcast"]

    name = db.Column(db.String(128), nullable=False)
    leader = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    kingdom_id = db.Column(db.Integer, db.ForeignKey('kingdom.id'), nullable=False)
    vote = db.Column(db.Integer)
    last_vote_date = db.Column(db.DateTime)

    _land = db.Column(db.Integer)
    race = db.Column(db.String(32))
    gender = db.Column(db.String(16))
    tax = db.Column(db.Integer)
    _gold = db.Column(db.Integer)
    _wood = db.Column(db.Integer)
    _iron = db.Column(db.Integer)
    rations = db.Column(db.Float)
    _happiness = db.Column(db.Integer)  # Out of 100
    _population = db.Column(db.Integer)
    _hunger = db.Column(db.Integer)  # Out of 100
    weather = db.Column(db.String(32))
    title = db.Column(db.String(32))
    production = db.Column(db.Integer)
    grain_stores = db.Column(db.Integer)
    notifications = db.relationship('Notification', backref='kingdom')

    expeditions = db.relationship('Expedition', backref='county')
    infiltrations = db.relationship('Infiltration', backref='county')

    births = db.Column(db.Integer)
    deaths = db.Column(db.Integer)
    immigration = db.Column(db.Integer)
    emigration = db.Column(db.Integer)

    buildings = db.relationship("Building",
                                collection_class=attribute_mapped_collection('base_name'),
                                cascade="all, delete, delete-orphan", passive_deletes=True)
    armies = db.relationship("Army",
                             collection_class=attribute_mapped_collection('base_name'),
                             cascade="all, delete, delete-orphan", passive_deletes=True)

    def __init__(self, name, leader, user_id, race, gender):

        self.name = name
        self.leader = leader
        self.user_id = user_id
        self.kingdom_id = randint(1, len(kingdom_names))
        self.race = race
        self.gender = gender
        self.title = 'Engineer'
        self.vote = None
        self.last_vote_date = None

        self._population = 500
        self._land = 150
        self._hunger = 75
        self._happiness = 75
        self.tax = 5
        self._gold = 1000
        self._wood = 100
        self._iron = 25
        self.rations = 1
        self.production = 0  # How many buildings you can build per day
        self.grain_stores = 0
        self.weather = "Sunny"

        self.births = 0
        self.deaths = 0
        self.immigration = 0
        self.emigration = 0

        buildings = None
        armies = None
        if self.race == 'Dwarf':
            buildings = deepcopy(dwarf_buildings)
            armies = deepcopy(dwarf_armies)
        elif self.race == 'Human':
            buildings = deepcopy(human_buildings)
            armies = deepcopy(human_armies)
        self.buildings = buildings
        self.armies = armies

    @property
    def population(self):
        return self._population

    @population.setter
    def population(self, value):
        self._population = value
        self.check_incremental_achievement("population", self._population)

    @property
    def land(self):
        return self._land

    @land.setter
    def land(self, value):
        difference = value - self._land
        if value <= 0:
            return "YOU LOST THE GAME"
        if difference < 0:
            self.destroy_buildings(self, abs(difference))
        self._land = value
        self.check_incremental_achievement("land", self._land)

    @property
    def gold(self):
        return self._gold

    @gold.setter
    def gold(self, value):
        self._gold = value
        self.check_incremental_achievement("gold", self._gold)

    @property
    def wood(self):
        return self._wood

    @wood.setter
    def wood(self, value):
        self._wood = value
        self.check_incremental_achievement("wood", self._wood)

    @property
    def iron(self):
        return self._iron

    @iron.setter
    def iron(self, value):
        self._iron = value
        self.check_incremental_achievement("iron", self._iron)

    @property
    def happiness(self):
        return self._happiness

    @happiness.setter
    def happiness(self, value):
        self._happiness = value

    @property
    def hunger(self):
        return self._hunger

    @hunger.setter
    def hunger(self, value):
        self._hunger = int(min(max(value, 1), 100))

    def check_incremental_achievement(self, name, amount):
        # Currently this does nothing but it's here for flexibility.
        self.user.check_incremental_achievement(name, amount)

    def get_available_land(self):
        """
        How much land you have which is empty and can be built upon.
        """
        return max(self.land - sum(building.total + building.pending for building in self.buildings.values()), 0)

    def get_votes_for_self(self):
        """
        Checks how many counties have voted for you to be king
        """
        return County.query.filter_by(vote=self.id, kingdom_id=self.kingdom.id).count()

    def can_vote(self):
        if self.last_vote_date and datetime.now() > (self.last_vote_date - timedelta(hours=24)):
            return False
        else:
            return True

    def cast_vote(self, vote):
        self.vote = vote
        self.last_vote_date = datetime.now()
        self.kingdom.count_votes()

    def display_vote(self):
        vote = County.query.filter_by(id=self.vote).first()
        return vote.name

    def get_army_size(self):
        return sum(army.total + army.currently_training for army in self.armies.values())

    def get_available_army_size(self):
        return sum(army.available for army in self.armies.values())

    def get_training_army_size(self):
        return sum(army.currently_training for army in self.armies.values())

    def get_unavailable_army_size(self):
        return sum(army.traveling for army in self.armies.values())

    def get_maintenance_workers(self):
        """
        Returns the population who are maintaining current buildings.
        """
        return sum(building.labour_maintenance * building.total for building in self.buildings.values())

    def get_available_workers(self):
        """
        Returns the population with no current duties.
        """
        return max(self.population - self.get_maintenance_workers() - self.get_army_size(), 0)

    def get_production_modifier(self):
        """
        Returns the modifier for how much production each worker produces.
        # Think about moving this to its own file or putting into a Race object or something
        """
        modifier = {'Base': 1}
        if self.race == 'Dwarf':
            modifier['Racial Bonus'] = 0.1
        if self.title == 'Engineer':
            modifier['Profession Bonus'] = 0.15
        return sum(modifier.values())

    def get_offensive_strength(self, army=None, county=None, traveling=False):
        """
        Returns the attack power of your army. If no army is sent in, it checks the full potential of the county.
        """
        strength = 0
        if army:
            for unit in self.armies.values():
                strength += army[unit.base_name] * unit.attack
        elif county:
            for unit in county.armies.values():
                strength += unit.available * unit.attack
        return int(strength)

    def get_defensive_strength(self):
        modifier = (self.buildings['forts'].output * self.buildings['forts'].total) + 1
        strength = 0
        for unit in self.armies.values():
            strength += unit.available * unit.defence
        strength += self.population // 25  # Every 25 population is 1 defence power
        strength *= modifier
        return int(strength)

    def get_casualties(self, attack_power, army={}):
        """
        Maybe move to a math transform file.
        army: For attacker, the army is passed in as dict. For defender, it's all active troops.
        ratio: The greater you outnumber the enemy, the safer your troops are.
        """
        casualties = 0
        hit_points_lost = randint(attack_power // 10, attack_power // 5)
        hit_points_to_be_removed = hit_points_lost
        if not army:  # ie. you are the defender and use entire army
            for unit in self.armies.values():
                available = unit.total - unit.traveling
                if available > 0:
                    available_hit_points = available * unit.health
                    this_units_damage = min(available_hit_points, hit_points_lost // 4)
                    hit_points_to_be_removed -= this_units_damage
                    this_dead = hit_points_to_be_removed // unit.health
                    unit.total -= this_dead
                    casualties += this_dead
            self.population -= hit_points_to_be_removed
            return casualties
        if army:
            stable_modifier = 1 - min((self.buildings['stables'].total / 100), 0)
            duration = max(sum(army.values()) * 0.04 * stable_modifier, 1)
            expedition = Expedition(self.id, duration)
            expedition.save()
            while hit_points_to_be_removed > 0:
                army = {key: value for key, value in army.items() if value > 0}  # Remove dead troops
                if army == {}:
                    break
                unit = choice(list(army))
                hit_points_to_be_removed -= self.armies[unit].health
                self.armies[unit].total -= 1
                casualties += 1
                army[unit] -= 1
            for unit in army.keys():
                self.armies[unit].traveling = army[unit]  # Surviving troops are marked as absent
                setattr(expedition, unit, army[unit])
        return casualties, expedition

    def destroy_buildings(self, county, land_destroyed):
        destroyed = randint(0, county.get_available_land()) # The more available land, the less likely building are destroyed
        need_list = True
        while destroyed < land_destroyed:
            if need_list:
                building_choices = [building for building in county.buildings.keys() if county.buildings[building].total > 0]
                if len(building_choices) == 0:
                    break
                need_list = False
            this_choice = choice(building_choices)
            county.buildings[this_choice].total -= 1
            if county.buildings[this_choice].total == 0:
                need_list = True
            destroyed += 1

    def battle_results(self, army, enemy):
        offence = self.get_offensive_strength(army=army)
        defence = enemy.get_defensive_strength()
        offence_casaulties, expedition = self.get_casualties(attack_power=defence, army=army)
        defence_casaulties = enemy.get_casualties(attack_power=offence)
        if offence > defence:
            land_gained = int(enemy.land * 0.1)
            expedition.land_acquired = land_gained
            enemy.land -= land_gained
            notification = Notification(enemy.id,
                                        "You were attacked by {}".format(self.name),
                                        "You lost {} acres and {} troops.".format(land_gained, defence_casaulties),
                                        self.kingdom.world.day)
            message = "You had {} power versus the enemies {} power. You were victorious! You gained {} acres" \
                      " but lost {} troops.".format(offence, defence, land_gained, offence_casaulties)
        else:
            notification = Notification(enemy.id,
                                        "You were attacked by {}".format(self.name),
                                        "You won the battle but lost {} troops.".format(defence_casaulties),
                                        self.kingdom.world.day)
            message = "You had {} power versus the enemies {} power. You failed and lost {} troops".format(offence,
                                                                                                           defence,
                                                                                                           offence_casaulties)
        notification.save()
        return message

    def advance_day(self):
        """
        Add a WORLD. Tracks day. Has game clock.
        """
        self.collect_taxes()
        self.production = self.get_production()
        self.produce_pending_buildings()
        self.produce_pending_armies()
        self.update_food()
        self.update_weather()
        self.update_population()
        expeditions = Expedition.query.filter_by(county_id=self.id).all()
        for expedition in expeditions:
            if expedition.duration > 0:
                expedition.duration -= 1
                if expedition.duration == 0:
                    self.armies['peasant'].traveling -= expedition.peasant
                    self.armies['archer'].traveling -= expedition.archer
                    self.armies['soldier'].traveling -= expedition.soldier
                    self.armies['elite'].traveling -= expedition.elite
                    self.land += expedition.land_acquired
                    notification = Notification(self.id, "Your army has returned",
                                                "{} new land has been added to your kingdom".format(expedition.land_acquired),
                                                self.kingdom.world.day)
                    notification.save()

    def display_news(self):
        events = [event for event in Notification.query.filter_by(county_id=self.id).all() if event.new is True]
        for event in events:
            event.new = False
        return events

    def get_gold_income(self):
        return int((self.population * (self.tax / 100)) + self.production)

    def get_wood_income(self):
        return self.buildings['mills'].total * self.buildings['mills'].output

    def get_iron_income(self):
        return self.buildings['mines'].total * self.buildings['mines'].output

    def get_death_rate(self):
        modifier = 1
        death_rate = uniform(1.5, 2.0) / self.hunger
        return int(death_rate * self.population * modifier)

    def get_birth_rate(self):
        modifier = {"Base": 1}
        if self.race == 'Elf':
            modifier['Racial Bonus'] = -0.1
        if self.title == 'Goblin':
            modifier['Racial Bonus'] = 0.15
        modifier = sum(modifier.values()) * uniform(0.9995, 1.0005)
        birth_rate = self.buildings['houses'].total * self.buildings['houses'].output
        return int(birth_rate * modifier)

    def get_immigration_rate(self):
        return randint(20, 30)

    def get_emmigration_rate(self):
        return randint(100, 110 + self.kingdom.world.age) - self.happiness

    def get_population_change(self, prediction=False):
        if prediction:
            seed(self.kingdom.world.day)
        growth = self.get_birth_rate() + self.get_immigration_rate()
        decay = self.get_death_rate() + self.get_emmigration_rate()
        return growth - decay

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
                 and building.production_cost <= self.production]
        if queue and self.production > 0:
            building = choice(queue)
            building.pending -= 1
            building.total += 1
            self.production -= building.production_cost
            self.produce_pending_buildings()

    def produce_pending_armies(self):
        """
        Chooses each unit that can be produced. Chooses each one and loops through the maximum amount.
        Keeps building one until you can't or don't want to, then breaks the loop.
        """
        for unit in self.armies.values():
            for i in range(unit.currently_training):
                if unit.currently_training > 0:
                    unit.currently_training -= 1
                    unit.total += 1
                else:
                    break

    def update_weather(self):
        self.weather = choice(self.weather_choices)
        if self.weather == 'stormy':
            notification = Notification(self.id, "Storms have ravaged your crops",
                                        "You lost 20 bushels of wheat.", self.kingdom.world.day)
            self.grain_stores = max(self.grain_stores - 20, 0)
            notification.save()

    def update_food(self):
        total_food = self.get_produced_dairy() + self.get_produced_grain() + self.grain_stores
        food_eaten = self.get_food_to_be_eaten()
        if total_food >= food_eaten:
            self.grain_stores += min(self.get_produced_dairy() + self.get_produced_grain() - food_eaten, self.get_produced_grain())
            self.hunger = self.hunger + 1
        else:
            self.grain_stores = 0
            self.hunger -= (food_eaten / total_food) * 5

    def get_produced_grain(self):
        return self.buildings['fields'].total * self.buildings['fields'].output

    def get_produced_dairy(self):
        return self.buildings['pastures'].total * self.buildings['pastures'].output
    
    def get_food_to_be_eaten(self):
        return int(self.population * self.rations)
    
    def grain_storage_change(self):
        food_produced = self.get_produced_dairy() + self.get_produced_grain()
        food_delta = food_produced - self.get_food_to_be_eaten()
        if food_delta > 0:  # If you have food left over, save it with a max of how much grain you produced
            return min(food_delta, self.get_produced_grain())
        return food_delta

    def update_population(self):
        self.deaths = self.get_death_rate()
        self.emigration = self.get_emmigration_rate()
        self.births = self.get_birth_rate()
        self.immigration = self.get_immigration_rate()
        self.population += (self.births + self.immigration) - (self.deaths + self.emigration)

    def get_production(self):
        return max(int(self.get_production_modifier() * self.get_available_workers() / 3), 0)

    def get_thieves_availability(self, day):
        current_report = Infiltration.query.filter_by(county_id=self.id).first()
        if not current_report or (current_report.day + current_report.duration <= day):
            return True
        else:
            return False

    def get_thieves_report(self, target_id):
        return Infiltration.query.filter_by(county_id=self.id, target_id=target_id).first()

    def get_future_thief_report_duration(self):
        modifier = 1 - (self.buildings['guilds'].total / self.land)
        return int(24 * modifier)

    def get_current_thief_report_duration(self, day):
        current_report = Infiltration.query.filter_by(county_id=self.id).first()
        return current_report.day + current_report.duration - day

    def get_expeditions(self):
        expeditions = Expedition.query.filter_by(county_id=self.id).all()
        return [expedition for expedition in expeditions if expedition.duration > 0]

    @property
    def hunger_terminology(self):
        if self.hunger < 20:
            return "dying of hunger"
        if self.hunger < 50:
            return "starving"
        if self.hunger < 75:
            return "hungry"
        if self.hunger < 90:
            return "sated"
        return "well nourished"

    @property
    def happiness_terminology(self):
        if self.happiness < 20:
            return "rioting"
        if self.happiness < 50:
            return "furious"
        if self.happiness < 75:
            return "discontent"
        if self.happiness < 90:
            return "content"
        return "pleased"

    @property
    def rations_terminology(self):
        terminology_dictionary = {0: "None", 0.25: "Quarter", 0.5: "Half", 1: "Normal", 2: "Double", 3: "Triple"}
        return terminology_dictionary[self.rations]

    def __repr__(self):
        return '<County %r (%r)>' % (self.name, self.id)
