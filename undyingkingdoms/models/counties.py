import math
from datetime import datetime, timedelta
from random import choice, uniform, randint

from sqlalchemy import desc
from sqlalchemy.orm.collections import attribute_mapped_collection

from undyingkingdoms.models.bases import GameState, db
from undyingkingdoms.models.helpers import cached_random
from undyingkingdoms.models.notifications import Notification
from undyingkingdoms.models.expeditions import Expedition
from undyingkingdoms.models.infiltrations import Infiltration
from undyingkingdoms.models.preferences import Preferences
from undyingkingdoms.models.technologies import Technology
from undyingkingdoms.models.trades import Trade
from undyingkingdoms.static.metadata.metadata import birth_rate_modifier, food_consumed_modifier, death_rate_modifier, \
    income_modifier, production_per_worker_modifier, offensive_power_modifier, defense_per_citizen_modifier, \
    happiness_modifier, buildings_built_per_day_modifier

from copy import deepcopy

from undyingkingdoms.static.metadata.metadata_armies_dwarf import dwarf_armies
from undyingkingdoms.static.metadata.metadata_armies_elf import elf_armies
from undyingkingdoms.static.metadata.metadata_armies_goblin import goblin_armies
from undyingkingdoms.static.metadata.metadata_armies_human import human_armies
from undyingkingdoms.static.metadata.metadata_buildings_dwarf import dwarf_buildings
from undyingkingdoms.static.metadata.metadata_buildings_elf import elf_buildings
from undyingkingdoms.static.metadata.metadata_buildings_goblin import goblin_buildings
from undyingkingdoms.static.metadata.metadata_buildings_human import human_buildings
from undyingkingdoms.static.metadata.metadata_magic_all import generic_spells
from undyingkingdoms.static.metadata.metadata_magic_elf import elf_spells
from undyingkingdoms.static.metadata.metadata_research_all import generic_technology


class County(GameState):
    weather_choices = ["clear skies", "stormy", "sunny", "cloudy", "light rain", "overcast"]

    name = db.Column(db.String(128), nullable=False)
    leader = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    kingdom_id = db.Column(db.Integer, db.ForeignKey('kingdom.id'), nullable=False)
    day = db.Column(db.Integer)
    vote = db.Column(db.Integer)
    last_vote_date = db.Column(db.DateTime)

    messages = db.relationship('Message', backref='county')

    race = db.Column(db.String(32))
    title = db.Column(db.String(16))
    background = db.Column(db.String(32))

    _population = db.Column(db.Integer)
    _land = db.Column(db.Integer)
    _happiness = db.Column(db.Integer)  # Out of 100
    _nourishment = db.Column(db.Integer)  # Out of 100
    _health = db.Column(db.Integer)  # Out of 100

    _gold = db.Column(db.Integer)
    _wood = db.Column(db.Integer)
    _iron = db.Column(db.Integer)
    _stone = db.Column(db.Integer)
    _research = db.Column(db.Integer)
    _mana = db.Column(db.Integer)
    lifetime_gold = db.Column(db.Integer)
    lifetime_wood = db.Column(db.Integer)
    lifetime_iron = db.Column(db.Integer)
    lifetime_stone = db.Column(db.Integer)
    lifetime_research = db.Column(db.Integer)
    lifetime_mana = db.Column(db.Integer)

    weather = db.Column(db.String(32))
    grain_stores = db.Column(db.Integer)
    notifications = db.relationship('Notification', backref='county')

    expeditions = db.relationship('Expedition', backref='county')
    infiltrations = db.relationship('Infiltration', backref='county')

    produce_land = db.Column(db.Integer)  # Progress towards next land

    births = db.Column(db.Integer)
    deaths = db.Column(db.Integer)
    immigration = db.Column(db.Integer)
    emigration = db.Column(db.Integer)
    buildings = db.relationship("Building",
                                collection_class=attribute_mapped_collection('name'),
                                cascade="all, delete, delete-orphan", passive_deletes=True)
    armies = db.relationship("Army",
                             collection_class=attribute_mapped_collection('name'),
                             cascade="all, delete, delete-orphan", passive_deletes=True)
    technologies = db.relationship("Technology",
                                   collection_class=attribute_mapped_collection('name'),
                                   cascade="all, delete, delete-orphan", passive_deletes=True)
    spells = db.relationship("Spell",
                             collection_class=attribute_mapped_collection('name'),
                             cascade="all, delete, delete-orphan", passive_deletes=True)

    def __init__(self, kingdom_id, name, leader, user_id, race, title, background):
        self.name = name
        self.leader = leader
        self.user_id = user_id
        self.kingdom_id = kingdom_id
        self.race = race
        self.title = title
        self.background = background
        self.day = 0
        self.vote = None
        self.last_vote_date = None
        # Basic resources
        self._population = 500
        self._land = 150
        self._nourishment = 75
        self._happiness = 75
        self._health = 75
        self.weather = "Sunny"
        # Resources
        self._gold = 500
        self._wood = 100
        self._iron = 0
        self._stone = 0
        self._research = 0
        self._mana = 0
        self.grain_stores = 500
        self.produce_land = 0  # Progress towards next land
        # Lifetime accrued resources
        self.lifetime_gold = self._gold
        self.lifetime_wood = self._wood
        self.lifetime_iron = self._iron
        self.lifetime_stone = self._stone
        self.lifetime_research = self._research
        self.lifetime_mana = self._mana
        # Predictions from advisors
        self.births = 0
        self.deaths = 0
        self.immigration = 0
        self.emigration = 0
        # Buildings and Armies extracted from metadata
        self.spells = deepcopy(generic_spells)
        if self.race == 'Dwarf':
            self.buildings = deepcopy(dwarf_buildings)
            self.armies = deepcopy(dwarf_armies)
        elif self.race == 'Human':
            self.buildings = deepcopy(human_buildings)
            self.armies = deepcopy(human_armies)
        elif self.race == 'Elf':
            self.buildings = deepcopy(elf_buildings)
            self.armies = deepcopy(elf_armies)
            self.spells = deepcopy(elf_spells)
        elif self.race == 'Goblin':
            self.buildings = deepcopy(goblin_buildings)
            self.armies = deepcopy(goblin_armies)
        else:
            raise AttributeError('Buildings and Armies were not found in metadata')
        self.technologies = deepcopy(generic_technology)
        for building in self.buildings:
            self.buildings[building].update_description()

    @property
    def population(self):
        return self._population

    @population.setter
    def population(self, value):
        self._population = max(value, 1)
        self.check_incremental_achievement("population", self._population)

    @property
    def land(self):
        return self._land

    @land.setter
    def land(self, value):
        difference = value - self._land
        if value <= 0:
            self._land = "YOU LOST THE GAME"
        if difference < 0:
            self.destroy_buildings(self, abs(difference))
        self._land = value
        self.check_incremental_achievement("land", self._land)

    @property
    def gold(self):
        return self._gold

    @gold.setter
    def gold(self, value):
        difference = value - self._gold
        if difference > 0:
            self.lifetime_gold += difference
        self._gold = max(value, 0)
        self.check_incremental_achievement("gold", self._gold)

    @property
    def wood(self):
        return self._wood

    @wood.setter
    def wood(self, value):
        difference = value - self._wood
        if difference > 0:
            self.lifetime_wood += difference
        self._wood = max(value, 0)
        self.check_incremental_achievement("wood", self._wood)

    @property
    def iron(self):
        return self._iron

    @iron.setter
    def iron(self, value):
        difference = value - self._iron
        if difference > 0:
            self.lifetime_iron += difference
        self._iron = max(value, 0)
        self.check_incremental_achievement("iron", self._iron)

    @property
    def stone(self):
        return self._stone

    @stone.setter
    def stone(self, value):
        difference = value - self._stone
        if difference > 0:
            self.lifetime_stone += difference
        self._stone = max(value, 0)
        self.check_incremental_achievement("stone", self._stone)

    @property
    def research(self):
        return self._research

    @research.setter
    def research(self, value):
        difference = value - self._research
        if difference > 0:
            self.lifetime_research += difference
        self._research = max(value, 0)
        self.check_incremental_achievement("research", self._research)

    @property
    def mana(self):
        return self._mana

    @mana.setter
    def mana(self, value):
        difference = value - self._mana
        if difference > 0:
            self.lifetime_mana += difference
        self._mana = max(value, 0)
        self.check_incremental_achievement("mana", self._mana)

    @property
    def happiness(self):
        return self._happiness

    @happiness.setter
    def happiness(self, value):
        self._happiness = min(max(value, 1), 100)

    @property
    def nourishment(self):
        return self._nourishment

    @nourishment.setter
    def nourishment(self, value):
        self._nourishment = int(min(max(value, 1), 100))

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = int(min(max(value, 1), 100))

    @property
    def tax_rate(self):
        return Preferences.query.filter_by(county_id=self.id).first().tax_rate

    @tax_rate.setter
    def tax_rate(self, value):
        preference = Preferences.query.filter_by(county_id=self.id).first()
        preference.tax_rate = value

    @property
    def rations(self):
        return Preferences.query.filter_by(county_id=self.id).first().rations

    @rations.setter
    def rations(self, value):
        preference = Preferences.query.filter_by(county_id=self.id).first()
        preference.rations = value

    @property
    def production_choice(self):
        return Preferences.query.filter_by(county_id=self.id).first().production_choice

    @production_choice.setter
    def production_choice(self, value):
        preference = Preferences.query.filter_by(county_id=self.id).first()
        preference.production_choice = value

    @property
    def research_choice(self):
        return Preferences.query.filter_by(county_id=self.id).first().research_choice

    @research_choice.setter
    def research_choice(self, value):
        preference = Preferences.query.filter_by(county_id=self.id).first()
        preference.research_choice = value

    @property
    def seed(self):
        return self.kingdom.world.day

    # Voting
    def get_votes_for_self(self):
        """
        Checks how many counties have voted for you to be king
        """
        return County.query.filter_by(vote=self.id, kingdom_id=self.kingdom.id).count()

    def can_vote(self):
        if self.last_vote_date and datetime.utcnow() > (self.last_vote_date - timedelta(hours=24)):
            return False
        else:
            return True

    def cast_vote(self, vote):
        self.vote = vote
        self.last_vote_date = datetime.utcnow()
        self.kingdom.count_votes()

    def display_vote(self):
        vote = County.query.get(self.vote)
        return vote.name

    # Advance day
    def advance_day(self):
        """
        Add a WORLD. Tracks day. Has game clock.
        """
        self.update_daily_resources()
        self.advance_research()
        self.produce_pending_buildings()
        self.produce_pending_armies()
        self.apply_excess_production_value()
        self.update_food()
        self.update_population()
        self.update_weather()  # Is before random events because they can affect weather
        self.get_random_daily_events()

        expeditions = Expedition.query.filter_by(county_id=self.id).filter(Expedition.duration > 0).all()
        for expedition in expeditions:
            expedition.duration -= 1
            if expedition.duration == 0:
                self.armies['peasant'].traveling -= expedition.peasant
                self.armies['soldier'].traveling -= expedition.soldier
                self.armies['elite'].traveling -= expedition.elite
                self.armies['monster'].traveling -= expedition.monster
                self.land += expedition.land_acquired
                notification = Notification(self.id, "Your army has returned",
                                            "{} new land has been added to your county".format(
                                                expedition.land_acquired),
                                            self.kingdom.world.day)
                notification.save()

        trades = Trade.query.filter_by(county_id=self.id).filter_by(status='Pending').filter(Trade.duration > 0).all()
        for trade in trades:
            trade.duration -= 1
            if trade.duration == 0:
                self.gold += trade.gold_to_give
                self.wood += trade.wood_to_give
                self.iron += trade.iron_to_give
                self.stone += trade.stone_to_give
                self.grain += trade.grain_to_give
                target_county = County.query.get(trade.target_id)
                notification = Notification(self.id, "Trade Offer",
                                            "Your trade offer to {} has expired and your resources have been return".format(
                                                target_county.name), self.kingdom.world.day)
                notification.save()

        infiltrations = Infiltration.query.filter_by(county_id=self.id).filter(Infiltration.duration > 0).all()
        for infiltration in infiltrations:
            infiltration.duration -= 1

        self.day += 1

    def temporary_bot_tweaks(self):
        if randint(1, 10) == 10 and self.day > 10:
            self.land += randint(-5, 15)
        if randint(1, 10) == 10:
            self.armies['peasant'].total += randint(1, 4)
            self.armies['soldier'].total += randint(1, 3)
            self.armies['archer'].total += randint(1, 2)
            self.armies['elite'].total += 1
        if randint(1, 10) > 8:
            self.gold -= 25
        if randint(1, 24) == 24 and self.kingdom.leader == 0:
            friendly_counties = County.query.filter_by(kingdom_id=self.kingdom_id).all()
            friendly_counties = [county for county in friendly_counties if not county.user.is_bot]
            self.vote = choice(friendly_counties).id
            self.kingdom.count_votes()
        if randint(1, 5) == 5:
            self.buildings['house'].total += 2
            self.buildings['field'].total += 1
            self.buildings['pasture'].total += 1

    def update_daily_resources(self):
        self.gold += self.get_gold_change()
        self.wood += self.get_wood_income()
        self.iron += self.get_iron_income()
        self.stone += self.get_stone_income()
        self.mana += self.get_mana_change()
        self.research += self.get_research_change()
        self.happiness += self.get_happiness_change()
        self.health += self.get_health_change()

    def advance_research(self):
        technology = self.technologies[self.research_choice]
        technology.current += self.research
        print("Research", technology.current, technology.required, self.research)
        if technology.current >= technology.required:  # You save left over research
            self.research = technology.current - technology.required
            technology.completed = True
            available_technologies = Technology.query.filter_by(county_id=self.id).filter_by(completed=False).first()
            self.research_choice = available_technologies.name
        else:  # You don't keep research as a resource; it's spent
            self.research = 0

    def get_health_change(self):
        if self.nourishment > 90:
            return 2
        elif self.nourishment > 80:
            return 1
        elif self.nourishment > 70:
            return 0
        elif self.nourishment > 60:
            return -1
        elif self.nourishment > 50:
            return -2
        elif self.nourishment > 40:
            return -3
        return -4

    def get_happiness_change(self):
        change = 7 - self.tax_rate
        if self.production_choice == 3:
            change += self.get_excess_production_value(self.production_choice)
        modifier = happiness_modifier.get(self.race, ("", 0))[1] + happiness_modifier.get(self.background, ("", 0))[1]
        return change + modifier

    def update_weather(self):
        self.weather = choice(self.weather_choices)

    def get_random_daily_events(self):
        random_chance = randint(1, 200)
        notification = None
        if random_chance == 1 and self.grain_stores > 0:
            amount = min(self.day * randint(1, 2), self.grain_stores)
            notification = Notification(self.id,
                                        "Rats have gotten into your grain silos",
                                        "Your county lost {} of its stored grain.".format(amount),
                                        self.kingdom.world.day)
            self.grain_stores -= amount

        elif random_chance == 2 and self.happiness > 90:
            amount = randint(100, 200)
            notification = Notification(self.id,
                                        "Your people celebrate your rule",
                                        "Your people hold a feast and offer you {} gold as tribute.".format(amount),
                                        self.kingdom.world.day)
            self.gold += amount

        elif random_chance == 3 and self.buildings['pasture'].total > 0:
            amount = min(randint(3, 6), self.buildings['pasture'].total)
            notification = Notification(self.id,
                                        "A disease has affected your cattle",
                                        "Your county has lost {} of its dairy farms.".format(amount),
                                        self.kingdom.world.day)
            self.buildings['pasture'].total -= amount

        elif random_chance == 4 and self.buildings['field'].total > 0:
            amount = min(randint(2, 4), self.buildings['field'].total)
            notification = Notification(self.id,
                                        "Storms have ravaged your crops",
                                        "A massive storm has destroyed {} of your fields.".format(amount),
                                        self.kingdom.world.day)
            self.buildings['field'].total -= amount
            self.weather = 'thunderstorm'

        elif random_chance == 5 and self.buildings['field'].total > 0:
            amount = self.buildings['field'].total * 3
            notification = Notification(self.id,
                                        "Booster crops",
                                        "Due to excellent weather this season, your crops produced an addition {} grain today.".format(
                                            amount),
                                        self.kingdom.world.day)
            self.grain_stores += amount
            self.weather = 'lovely'

        elif random_chance == 6:
            modifier = ((101 - self.nourishment) // 20 + 1) / 100  # Percent of people who will die (1% -> 5%)
            amount = int(modifier * self.population)
            notification = Notification(self.id,
                                        "Black Death",
                                        "A plague has swept over our county, killing {} of our people.".format(amount),
                                        self.kingdom.world.day)
            self.population -= amount

        elif random_chance == 7 and self.buildings['house'].total > 0:
            amount = min(randint(2, 4), self.buildings['house'].total)
            notification = Notification(self.id,
                                        "Disaster",
                                        "A fire has spread in the city burning down {} of your {}.".format(amount,
                                                                                                           self.buildings[
                                                                                                               'house'].class_name),
                                        self.kingdom.world.day)
            self.buildings['house'].total -= amount

        elif random_chance == 8:
            amount = min(randint(3, 7), self.nourishment)
            notification = Notification(self.id,
                                        "Sickness",
                                        "A disease has spread throughout your lands, lowering your county's health by {}.".format(
                                            amount), self.kingdom.world.day)
            self.health -= amount

        if notification:
            notification.save()

    def get_nourishment_change(self):
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

    def update_food(self):
        total_food = self.get_produced_dairy() + self.get_produced_grain() + self.grain_stores + self.get_excess_worker_produced_food()
        food_eaten = self.get_food_to_be_eaten()
        if total_food >= food_eaten:
            # If you have enough food, you lose it and your nourishment changes based on rations
            self.grain_stores += min(self.get_produced_dairy() + self.get_produced_grain() - food_eaten,
                                     self.get_produced_grain())
            self.nourishment += self.get_nourishment_change()
        else:
            # If you don't have enough food, you lose it all and lose nourishment based on leftover people
            self.grain_stores = 0
            hungry_people = food_eaten - total_food
            nourishment_loss = (hungry_people // 200) + 1  # 1 plus 1 for every 200 unfed people
            self.nourishment -= min(nourishment_loss, 5)

    def get_produced_grain(self):
        modifier = 1
        if self.technologies['agriculture'].completed:
            modifier += 0.5
        return int(self.buildings['field'].total * self.buildings['field'].output * modifier)

    def get_produced_dairy(self):
        modifier = 1
        if self.technologies['animal husbandry'].completed:
            modifier += 0.5
        return int(self.buildings['pasture'].total * self.buildings['pasture'].output * modifier)

    def get_excess_worker_produced_food(self):
        if self.production_choice == 2:
            return self.get_excess_production_value(self.production_choice)
        else:
            return 0

    def get_food_to_be_eaten(self):
        modifier = 1 + food_consumed_modifier.get(self.race, ("", 0))[1] + \
                   food_consumed_modifier.get(self.background, ("", 0))[1]
        return int((self.population - self.get_unavailable_army_size()) * self.rations * modifier)

    def grain_storage_change(self):
        food_produced = self.get_produced_dairy() + self.get_produced_grain() + self.get_excess_worker_produced_food()
        food_delta = food_produced - self.get_food_to_be_eaten()
        if food_delta > 0:  # If you have food left over, save it with a max of how much grain you produced
            return int(min(food_delta, self.get_produced_grain()))
        return int(max(food_delta, - self.grain_stores))

    # Land
    def get_available_land(self):
        """
        How much land you have which is empty and can be built upon.
        """
        return max(self.land - sum(building.total + building.pending for building in self.buildings.values()), 0)

    # Workers / Population / Soldiers
    def get_army_size(self):
        return sum(army.total + army.currently_training for army in self.armies.values())

    def get_available_army_size(self):
        return sum(army.available for army in self.armies.values())

    def get_training_army_size(self):
        return sum(army.currently_training for army in self.armies.values())

    def get_unavailable_army_size(self):
        return sum(army.traveling for army in self.armies.values())

    def get_employed_workers(self):
        """
        Returns the population who are maintaining current buildings.
        """
        return sum(building.workers_employed * building.total for building in self.buildings.values())

    def get_available_workers(self):
        """
        Returns the population with no current duties.
        """
        return max(self.population - self.get_employed_workers() - self.get_army_size(), 0)

    def get_death_rate(self):
        modifier = 1 + death_rate_modifier.get(self.race, ("", 0))[1] + \
                   death_rate_modifier.get(self.background, ("", 0))[1]
        death_rate = (uniform(1.7, 2.1) / self.health) * modifier
        return int(death_rate * self.population)

    def get_birth_rate(self):
        modifier = 1 + birth_rate_modifier.get(self.race, ("", 0))[1] + \
                   birth_rate_modifier.get(self.background, ("", 0))[1]
        birth_rate = self.buildings['house'].total * self.buildings['house'].output * modifier
        return int(birth_rate * uniform(0.9995, 1.0005))

    @staticmethod
    def get_immigration_rate():
        return randint(25, 35)

    def get_emigration_rate(self):
        return randint(100, 110 + self.kingdom.world.age) - self.happiness

    @cached_random
    def get_population_change(self, prediction=False):
        growth = self.get_birth_rate() + self.get_immigration_rate()
        decay = self.get_death_rate() + self.get_emigration_rate()
        return growth - decay

    def update_population(self):
        self.deaths = self.get_death_rate()
        self.emigration = self.get_emigration_rate()
        self.births = self.get_birth_rate()
        self.immigration = self.get_immigration_rate()
        self.population += (self.births + self.immigration) - (self.deaths + self.emigration)

    # Resources
    def get_tax_income(self):
        return int(self.population * (self.tax_rate / 100))

    def get_bank_income(self):
        return self.buildings['bank'].total * self.buildings['bank'].output

    def get_upkeep_costs(self):
        return sum(unit.upkeep * unit.total for unit in self.armies.values()) // 24

    def get_gold_change(self):
        modifier = 1 + income_modifier.get(self.race, ("", 0))[1] \
                   + income_modifier.get(self.background, ("", 0))[1]
        if self.production_choice == 0:
            excess_worker_income = self.get_excess_production_value(self.production_choice)
        else:
            excess_worker_income = 0
        income = (self.get_tax_income() + self.get_bank_income() + excess_worker_income) * modifier
        revenue = self.get_upkeep_costs()
        return int(income - revenue)

    def get_wood_income(self):
        return self.buildings['mill'].total * self.buildings['mill'].output

    def get_iron_income(self):
        return self.buildings['mine'].total * self.buildings['mine'].output

    def get_stone_income(self):
        return self.buildings['quarry'].total * self.buildings['quarry'].output

    def get_mana_change(self):
        return self.buildings['arcane'].total * self.buildings['arcane'].output

    def get_research_change(self):
        return self.buildings['lab'].total * self.buildings['lab'].output

    # Building
    def get_production_modifier(self):  # Modifiers your excess production
        return 1 + production_per_worker_modifier.get(self.race, ("", 0))[1] \
               + production_per_worker_modifier.get(self.background, ("", 0))[1]

    def get_excess_production(self):
        """
        Returns the amount of excess production you get each turn
        """
        return max(int(self.get_production_modifier() * self.get_available_workers()), 0)

    def get_excess_production_value(self, value=-1):
        """
        Users the excess production towards completing a task
        """
        if value == -1:
            excess_worker_choice = self.production_choice
        else:
            excess_worker_choice = value
        if excess_worker_choice == 0:  # Gold
            return self.get_excess_production() // 14
        if excess_worker_choice == 1:  # Land
            return self.get_excess_production()
        if excess_worker_choice == 2:  # Food
            return self.get_excess_production() // 7
        if excess_worker_choice == 3:  # Happiness
            return 1

    def apply_excess_production_value(self):
        if self.production_choice == 0:
            self.gold += self.get_excess_production_value()
        if self.production_choice == 1:
            self.produce_land += self.get_excess_production_value()
            # Every 1000 production towards land gives you one acre
            if self.produce_land >= 2000:
                self.produce_land -= 2000
                self.land += 1
        if self.production_choice == 2:
            self.grain_stores += self.get_excess_production_value()
        if self.production_choice == 3:
            pass  # Already handled in self.get_happiness_change()

    def get_number_of_buildings_produced_per_day(self):
        amount = 3 + buildings_built_per_day_modifier.get(self.race, ("", 0))[1] \
                                + buildings_built_per_day_modifier.get(self.background, ("", 0))[1]
        if self.technologies['engineering'].completed:
            amount += 1
        return amount

    def produce_pending_buildings(self):
        """
        Gets a list of all buildings which can be built today. Builds it. Then recalls function.
        """
        buildings_to_be_built = self.get_number_of_buildings_produced_per_day()
        while buildings_to_be_built > 0:
            buildings_to_be_built -= 1
            queue = [building for building in self.buildings.values() if building.pending > 0]
            if queue:
                building = choice(queue)
                building.pending -= 1
                building.total += 1
            else:
                break

    def produce_pending_armies(self):
        """
        Chooses each unit that can be produced. Chooses each one and loops through the maximum amount.
        Keeps building one until you can't or don't want to, then breaks the loop.
        """
        for unit in self.armies.values():
            trainable = unit.trainable_per_day
            for i in range(unit.currently_training):
                if unit.currently_training > 0 and trainable > 0:
                    unit.currently_training -= 1
                    unit.total += 1
                    trainable -= 1
                else:
                    break

    # Battling
    def get_offensive_strength(self, army=None, county=None, scoreboard=False):
        """
        Returns the attack power of your army. If no army is sent in, it checks the full potential of the county.
        params: scoreboard - Looks at total possible power, even for troops who are unavailable
        """
        strength = 0
        modifier = 1 + offensive_power_modifier.get(self.race, ("", 0))[1] \
                   + offensive_power_modifier.get(self.background, ("", 0))[1]
        if self.technologies['steel'].completed:
            modifier += 0.2
        if army:
            for unit in self.armies.values():
                if unit.name != 'archer':
                    strength += army[unit.name] * unit.attack
        elif county:
            for unit in county.armies.values():
                if scoreboard:
                    strength += unit.total * unit.attack
                else:
                    strength += unit.available * unit.attack
        return int(strength * modifier)

    def get_defensive_strength(self, scoreboard=False):
        # First get base strength of citizens
        modifier = 1 + defense_per_citizen_modifier.get(self.race, ("", 0))[1] \
                   + defense_per_citizen_modifier.get(self.background, ("", 0))[1]
        strength = (self.population // 20) * modifier
        # Now add strength of soldiers at home
        for unit in self.armies.values():
            if scoreboard:
                strength += unit.total * unit.defence
            else:
                strength += unit.available * unit.defence
        # Lastly, multiply by the defensive building modifier
        strength *= (self.buildings['fort'].output * self.buildings['fort'].total) / 100 + 1
        return int(strength)

    def get_army_duration(self, army_size):
        base_duration = 2 + army_size // 20
        stables_modifier = 100 / (self.buildings['stables'].total * self.buildings['stables'].output + 100)
        return int(max(base_duration * stables_modifier, 3))

    def get_casualties(self, attack_power, army=(), enemy_id=-1, results="Draw"):
        """
        Maybe move to a math transform file.
        army: For attacker, the army is passed in as dict. For defender, it's all active troops.
        ratio: The greater you outnumber the enemy, the safer your troops are.
        """
        if army is ():
            army = {}
        casualties = 0
        hit_points_lost = randint(attack_power // 10, attack_power // 5)
        if results == "massive":
            hit_points_lost = randint(10, 20)
        elif results == "major":
            hit_points_lost *= 0.8
        hit_points_to_be_removed = hit_points_lost
        if not army:  # ie. you are the defender and use entire army
            for unit in self.armies.values():
                available = unit.available
                if available > 0:
                    available_hit_points = available * unit.health
                    this_units_damage = min(available_hit_points, hit_points_lost // 4)
                    hit_points_to_be_removed -= this_units_damage
                    this_dead = this_units_damage // unit.health
                    unit.total -= this_dead
                    casualties += this_dead
            self.population -= min(hit_points_to_be_removed, self.population)
            return casualties
        if army:
            hit_points_lost *= 1.25  # The attacker takes extra casualties
            duration = self.get_army_duration(sum(army.values()))
            expedition = Expedition(self.id, enemy_id, self.kingdom.world.day, self.day, duration, "attack")
            expedition.save()
            for unit in army.keys():
                setattr(expedition, unit + '_sent', army[unit])
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
                self.armies[unit].traveling += army[unit]  # Surviving troops are marked as absent
                setattr(expedition, unit, army[unit])
        return casualties, expedition

    def destroy_buildings(self, county, land_destroyed):
        destroyed = randint(0,
                            county.get_available_land())  # The more available land, the less likely building are destroyed
        need_list = True
        while destroyed < land_destroyed:
            if need_list:
                building_choices = [building for building in county.buildings.keys() if
                                    county.buildings[building].total > 0]
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
        percent_difference_in_power = abs(defence - offence) / ((defence + offence) / 2) * 100
        if percent_difference_in_power < 25:
            battle_word = "minor"
        elif percent_difference_in_power < 50:
            battle_word = "major"
        else:
            battle_word = "massive"
        offence_casaulties, expedition = self.get_casualties(attack_power=defence,
                                                             army=army,
                                                             enemy_id=enemy.id,
                                                             results=battle_word)
        defence_casaulties = enemy.get_casualties(attack_power=offence,
                                                  results=battle_word)
        if offence > defence:
            land_gained = max((enemy.land ** 3) * 0.1 / (self.land ** 2), 1)
            land_gained = int(min(land_gained, enemy.land * 0.2))
            expedition.land_acquired = land_gained
            enemy.land -= land_gained
            notification = Notification(enemy.id,
                                        "You were attacked by {} and suffered a {} loss.".format(self.name,
                                                                                                 battle_word),
                                        "You lost {} acres and {} troops in the battle.".format(land_gained,
                                                                                                defence_casaulties),
                                        self.kingdom.world.day)
            message = "You claimed a {} victory and gained {} acres, but lost {} troops in the battle.".format(
                battle_word,
                land_gained,
                offence_casaulties)
        else:
            notification = Notification(enemy.id,
                                        "You were attacked by {}".format(self.name),
                                        "You achieved a {} victory but lost {} troops.".format(battle_word,
                                                                                               defence_casaulties),
                                        self.kingdom.world.day)
            message = "You suffered a {} failure in battle and lost {} troops".format(battle_word, offence_casaulties)
        notification.save()
        return message

    # Achievements
    def check_incremental_achievement(self, name, amount):
        # Currently this does nothing but it's here for flexibility.
        self.user.check_incremental_achievement(name, amount)

    def display_news(self):
        events = [event for event in Notification.query.filter_by(county_id=self.id).all() if event.new is True]
        for event in events:
            event.new = False
        return events

    def display_old_news(self):
        events = [event for event in Notification.query.filter_by(county_id=self.id).all() if event.new is False]
        return events

    def get_total_number_of_thieves(self):
        return self.buildings['tavern'].total * self.buildings['tavern'].output

    # Infiltrations
    def get_number_of_available_thieves(self):
        all_current_missions = Infiltration.query.filter_by(county_id=self.id).filter(Infiltration.duration > 0).all()
        unavailable_thieves = sum(mission.amount_of_thieves for mission in all_current_missions)
        return self.get_total_number_of_thieves() - unavailable_thieves

    def get_thief_report_military(self, target_id):
        current_report = Infiltration.query.filter_by(county_id=self.id, target_id=target_id, success=True,
                                                      mission="scout military").order_by(desc('time_created')).first()
        return current_report

    def get_thief_report_infrastructure(self, target_id):
        current_report = Infiltration.query.filter_by(county_id=self.id, target_id=target_id,
                                                      mission="scout infrastructure").first()
        return current_report

    def get_expeditions(self):
        expeditions = Expedition.query.filter_by(county_id=self.id).all()
        return [expedition for expedition in expeditions if expedition.duration > 0]

    def get_chance_to_be_successfully_infiltrated(self):
        buffer_time = datetime.utcnow() - timedelta(hours=12)
        operations_on_target = Infiltration.query.filter_by(target_id=self.id).filter_by(success=True).filter(
            Infiltration.time_created > buffer_time).count()
        reduction = 10 + (self.get_number_of_available_thieves() * 3500 / self.land) ** 0.7 + (
                10 * operations_on_target)
        return max(int(100 - reduction), 10)

    # Terminology
    @property
    def nourishment_terminology(self):
        if self.nourishment < 20:
            return "dying of hunger"
        if self.nourishment < 50:
            return "starving"
        if self.nourishment < 75:
            return "hungry"
        if self.nourishment < 90:
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
    def health_terminology(self):
        if self.health < 20:
            return "diseased"
        if self.health < 50:
            return "sickly"
        if self.health < 75:
            return "average"
        if self.health < 90:
            return "hale"
        return "perfect"

    @property
    def rations_terminology(self):
        terminology_dictionary = {0: "None", 0.25: "Quarter", 0.5: "Half", 0.75: "Three Quarters",
                                  1: "Normal", 1.5: "One-and-a-half", 2: "Double", 3: "Triple"}
        return terminology_dictionary[self.rations]

    def __repr__(self):
        return '<County %r (%r)>' % (self.name, self.id)
