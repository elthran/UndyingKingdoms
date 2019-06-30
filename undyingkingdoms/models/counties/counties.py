import warnings
from datetime import datetime, timedelta
from random import choice, randint

from sqlalchemy import desc
from sqlalchemy.orm.collections import attribute_mapped_collection

from tests import bp
from undyingkingdoms.calculations.distributions import get_int_between_0_and_100, get_int_between_n_and_m
from undyingkingdoms.metadata.armies.metadata_armies_updater import update_armies
from ..magic import Casting
from ..bases import GameState, db
from .specifics import add_racial_data, add_background_data
from ..helpers import cached_random, extract_modifiers
from ..notifications import Notification
from ..expeditions import Expedition
from ..infiltrations import Infiltration
from ..trades import Trade
from undyingkingdoms.virtual_classes.all_metadata_imports import all_metadata_imports as md


class County(GameState):
    GOLD = 0
    LAND = 1
    FOOD = 2
    HAPPINESS = 3

    name = db.Column(db.String(128), nullable=False)
    leader = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    kingdom_id = db.Column(db.Integer, db.ForeignKey('kingdom.id'), nullable=False)
    day = db.Column(db.Integer)

    messages = db.relationship('Message', backref='county')

    race = db.Column(db.String(32))
    title = db.Column(db.String(16))
    background = db.Column(db.String(32))

    _population = db.Column(db.Integer)
    _land = db.Column(db.Integer)
    _happiness = db.Column(db.Integer)  # Out of 100
    _healthiness = db.Column(db.Integer)  # Out of 100

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

    grain_stores = db.Column(db.Integer)
    notifications = db.relationship('Notification', backref='county')

    expeditions = db.relationship('Expedition', backref='county')
    infiltrations = db.relationship('Infiltration', backref='county', foreign_keys='[Infiltration.county_id]')

    buildings = db.relationship(
        "Building",
        collection_class=attribute_mapped_collection('name'),
        cascade="all, delete, delete-orphan", passive_deletes=True
    )
    armies = db.relationship(
        "Army",
        collection_class=attribute_mapped_collection('name'),
        cascade="all, delete, delete-orphan", passive_deletes=True
    )
    magic = db.relationship(
        "Magic",
        collection_class=attribute_mapped_collection('name'),
        cascade="all, delete, delete-orphan", passive_deletes=True
    )

    preferences = db.relationship("Preferences", back_populates='county', uselist=False,
                                  foreign_keys="Preferences.county_id")

    def __init__(self, kingdom_id, name, leader, user, race, title, background):
        self.name = name
        self.leader = leader
        self.user = user
        self.kingdom_id = kingdom_id
        self.race = race
        self.title = title
        self.background = background
        self.day = 0
        # Basic resources
        self._population = 500
        self._land = 150
        self._healthiness = 75
        self._happiness = 100
        # Resources
        self._gold = 750
        self._wood = 250
        self._iron = 50
        self._stone = 0
        self._research = 0
        self._mana = 0
        self.grain_stores = 500
        # Lifetime accrued resources
        self.lifetime_gold = self._gold
        self.lifetime_wood = self._wood
        self.lifetime_iron = self._iron
        self.lifetime_stone = self._stone
        self.lifetime_research = self._research
        self.lifetime_mana = self._mana

        add_racial_data(self)
        self.armies = update_armies(self.background, self.armies)
        add_background_data(self)

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
        value = min(value, self.max_mana)
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
        self._happiness = get_int_between_n_and_m(value)

    @property
    def healthiness(self):
        return self._healthiness

    @healthiness.setter
    def healthiness(self, value):
        self._healthiness = get_int_between_n_and_m(value)

    @property
    def tax_rate(self):
        return self.preferences.tax_rate

    @tax_rate.setter
    def tax_rate(self, value):
        """Set tax rate.

        Tax rate has a flat reduction to happiness change.
        """
        self.preferences.tax_rate = value

    @property
    def rations(self):
        return self.preferences.rations

    @rations.setter
    def rations(self, value):
        self.preferences.rations = value

    @property
    def production_choice(self):
        return self.preferences.production_choice or 0

    @production_choice.setter
    def production_choice(self, choice):
        """Set the current production type.

        Production choice can modify happiness change.
        This works be happiness production is fixed.
        It won't work for gold because that might change between calls.
        """
        change = self.get_excess_production_value(choice)
        if self.production_choice != choice:
            # changing from happiness
            if self.production_choice == self.HAPPINESS:
                self.happiness_change -= self.get_excess_production_value(self.HAPPINESS)
            # changing to happiness
            if choice == self.HAPPINESS:
                self.happiness_change += change
        self.preferences.production_choice = choice

    @property
    def research_choice(self):
        return self.preferences.research_choice

    @research_choice.setter
    def research_choice(self, value):
        self.preferences.research_choice = value

    @property
    def spell_modifier(self):
        return 1 + (self.buildings["arcane"].total * self.buildings["arcane"].output / 100)

    @property
    def seed(self):
        return self.kingdom.world.day

    # Voting
    def can_vote(self):
        if self.preferences.last_vote_date and datetime.utcnow() > (
                self.preferences.last_vote_date - timedelta(hours=24)):
            return False
        else:
            return True

    def cast_vote(self, vote):
        self.preferences.vote = vote
        self.preferences.last_vote_date = datetime.utcnow()
        self.kingdom.count_votes()

    def display_vote(self):
        vote = self.preferences.vote
        return vote.name

    # Advance day
    def advance_day(self):
        """
        Add a WORLD. Tracks day. Has game clock.
        """
        event = self.event
        self.update_daily_resources()
        self.advance_research()
        self.produce_pending_buildings()
        self.produce_pending_armies()
        self.apply_excess_production_value()
        self.update_food()
        self.update_population()
        self.update_weather()  # Is before random events because they can affect weather
        event.build_random_daily_events(Notification)
        expeditions = Expedition.query.filter_by(county_id=self.id).filter(Expedition.duration > 0).all()
        for expedition in expeditions:
            expedition.duration -= 1
            if expedition.duration == 0:
                notification = Notification(
                    self,
                    "Your army has returned",
                    "Error: Report to admin",
                    "Military"
                )
                notification.save()
                self.armies['peasant'].traveling -= expedition.peasant
                self.armies['soldier'].traveling -= expedition.soldier
                self.armies['besieger'].traveling -= expedition.besieger
                self.armies['summon'].traveling -= expedition.summon
                self.armies['elite'].traveling -= expedition.elite
                self.armies['monster'].traveling -= expedition.monster
                self.land += expedition.land_acquired
                self.gold += expedition.gold_gained
                self.wood += expedition.wood_gained
                self.iron += expedition.iron_gained
                if expedition.mission == "Attack":
                    notification.content = f"{expedition.land_acquired} new land has been added to your county"
                elif expedition.mission == "Pillage":
                    notification.content = f"They have brought with them {expedition.gold_gained} gold, {expedition.wood_gained} wood, and {expedition.iron_gained} iron."
                elif expedition.mission == "Raze":
                    notification.content = f"They have successfully razed {expedition.land_razed} enemy acres."

        trades = Trade.query.filter_by(county_id=self.id).filter_by(status='Pending').filter(Trade.duration > 0).all()
        for trade in trades:
            trade.duration -= 1
            if trade.duration == 0:
                self.gold += trade.gold_to_give
                self.wood += trade.wood_to_give
                self.iron += trade.iron_to_give
                self.stone += trade.stone_to_give
                self.grain_stores += trade.grain_to_give
                target_county = trade.target
                notification = Notification(
                    self,
                    "Trade Offer",
                    f"Your trade offer to {target_county.name} has expired and your resources have been return",
                    "Trade"
                )
                notification.save()
        infiltrations = Infiltration.query.filter_by(county_id=self.id).filter(Infiltration.duration > 0).all()
        for infiltration in infiltrations:
            infiltration.duration -= 1
            if infiltration.duration == 0:
                notification = Notification(
                    self,
                    "Your thieves have returned",
                    "Error: Report to admin",
                    "Thieves"
                )
                notification.save()
                notification.content = f"Your {infiltration.amount_of_thieves} thieves have returned after their mission to {infiltration.mission}."

        spells = Casting.query.filter_by(target_id=self.id).filter(Casting.duration > 0).all()
        for spell in spells:
            spell.duration -= 1
            if spell.duration == 0:
                notification = Notification(
                    self,
                    "A spell has ended",
                    "Error: Report to admin",
                    "Magic"
                )
                notification.save()
                notification.content = f"{spell.name} has ended and is no longer affecting your county."

        self.day += 1

    def temporary_bot_tweaks(self):
        from undyingkingdoms.models.exports import User

        friendly_counties = County.query.join(User).filter(County.kingdom_id == self.kingdom_id, ~User.is_bot).all()
        if randint(1, 10) == 10 and self.day > 10:
            self.land += randint(-5, 15)
        if randint(1, 10) == 10:
            self.armies['peasant'].total += randint(1, 4)
            self.armies['soldier'].total += randint(1, 3)
            self.armies['archer'].total += randint(1, 2)
            self.armies['elite'].total += 1
        self.gold += randint(1, 6)
        self.wood += randint(1, 3)
        self.iron += 1
        if randint(1, 24) == 24 and self.kingdom.leader == 0 and friendly_counties:
            self.cast_vote(choice(friendly_counties))
        if randint(1, 10) == 10 and self.get_available_land() >= 5:
            self.buildings['house'].total += 3
            self.buildings['field'].total += 1
            self.buildings['pasture'].total += 1
        if randint(1, 12) == 12:
            trading_partner = choice(friendly_counties)
            trade_notice = Notification(
                trading_partner,
                "You were offered a trade",
                f"{self.name} has offered you a trade. Visit the trading page.",
                "Trade"
            )
            trade_notice.save()
            random = randint(1, 5)
            if random == 1:  # Send wood for gold
                trade_offered = Trade(self, trading_partner, self.kingdom.world.day, 24, 0, 40, 0, 0, 0, 60, 0, 0, 0,
                                      0)
                self.wood -= 40
            elif random == 2:  # Send iron for gold
                trade_offered = Trade(self, trading_partner, self.kingdom.world.day, 24, 0, 0, 30, 0, 0, 90, 0, 0, 0,
                                      0)
                self.iron -= 30
            elif random == 3:  # Send gold for iron and wood
                trade_offered = Trade(self, trading_partner, self.kingdom.world.day, 24, 120, 0, 0, 0, 0, 0, 40, 20,
                                      0, 0)
                self.gold -= 120
            elif random == 4:  # Send food for wood
                trade_offered = Trade(self, trading_partner, self.kingdom.world.day, 24, 0, 0, 0, 0, 750, 0, 0, 0, 0,
                                      50)
                self.gold -= 120
            else:  # Send food for iron
                trade_offered = Trade(self, trading_partner, self.kingdom.world.day, 24, 0, 0, 0, 0, 750, 0, 40, 20,
                                      0, 0)
                self.gold -= 120
            trade_offered.save()

    def update_daily_resources(self):
        self.gold += self.gold_income
        self.wood += self.get_wood_income()
        self.iron += self.iron_income
        self.stone += self.get_stone_income()
        self.mana += self.mana_change
        self.research += self.research_change
        self.happiness += self.happiness_change

    def update_weather(self):
        self.preferences.weather = choice(self.preferences.weather_choices)

    def get_healthiness_change(self):
        change = 0
        hungry_people = self.get_food_to_be_eaten() - self.grain_stores - self.get_produced_dairy() - self.get_produced_grain()

        noxious_fumes = Casting.query.filter_by(target_id=self.id, name="noxious_fumes").filter(
            (Casting.duration > 0) | (Casting.active == True)).all()
        if noxious_fumes:
            change += -3

        if hungry_people <= 0:  # You fed everyone
            if self.rations == 0:
                change += -6
            elif self.rations < 1:
                change += int(- 1 / self.rations - 1)
            else:
                change += int(self.rations * 2)
        else:  # You can't feed everyone
            change += -((hungry_people // 200) + 1)
        return change

    def update_food(self):
        total_food = self.get_produced_dairy() + self.get_produced_grain() + self.grain_stores + self.get_excess_worker_produced_food()
        food_eaten = self.get_food_to_be_eaten()
        if total_food >= food_eaten:
            # If you have enough food, you lose it and your healthiness changes based on rations
            self.grain_stores += min(self.get_produced_dairy() + self.get_produced_grain() - food_eaten,
                                     self.get_produced_grain())
            self.healthiness += self.get_healthiness_change()
        else:
            # If you don't have enough food, you lose it all and lose healthiness based on leftover people
            self.grain_stores = 0
            hungry_people = food_eaten - total_food
            healthiness_loss = (hungry_people // 200) + 1  # 1 plus 1 for every 200 unfed people
            self.healthiness -= min(healthiness_loss, 5)

    def get_produced_grain(self):
        warnings.warn("`get_produced_grain()` is deprecated, use attribute `produced_grain` instead.",
                      DeprecationWarning)
        return self.grain_produced

    def get_produced_dairy(self):
        warnings.warn("`get_produced_dairy()` is deprecated, use attribute `produced_dairy` instead.",
                      DeprecationWarning)
        return self.dairy_produced

    def get_excess_worker_produced_food(self):
        if self.production_choice == 2:
            return self.get_excess_production_value(self.production_choice)
        else:
            return 0

    def get_food_to_be_eaten(self):
        local_md = md['metadata']
        modifier = 1 + extract_modifiers(
            local_md.food_consumed_modifier,
            self.race,
            self.background
        )
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
    def get_workers_needed_to_be_efficient(self):
        if self.get_non_military_citizens() < self.get_employed_workers():
            return self.get_employed_workers() - self.get_non_military_citizens()
        return 0

    def building_efficiencies(self):
        return max(round((self.population - self.get_workers_needed_to_be_efficient()) / self.population, 2), 0.25)

    def get_army_size(self):
        return sum(army.total + army.currently_training for army in self.armies.values())

    def get_available_army_size(self):
        return sum(army.available for army in self.armies.values())

    def get_training_army_size(self):
        return sum(army.currently_training for army in self.armies.values())

    def get_unavailable_army_size(self):
        return sum(army.traveling for army in self.armies.values())

    def get_non_military_citizens(self):
        return self.population - self.get_army_size()

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
        local_md = md['metadata']
        modifier = 1 + extract_modifiers(
            local_md.death_rate_modifier,
            self.race,
            self.background
        )

        modify_death_rate = Casting.query.filter_by(target_id=self.id, name="modify_death_rate").filter(
            (Casting.duration > 0) | (Casting.active == True)).all()
        for spell in modify_death_rate or []:
            modifier += spell.output * self.spell_modifier

        death_rate = (2 / self.healthiness) * modifier

        return int(death_rate * self.population)

    def get_emigration_rate(self):
        return int(self.preferences.tax_rate + self.kingdom.world.age + (0.005 * self.population))

    @cached_random
    def get_population_change(self):
        growth = self.birth_rate + self.immigration_rate
        decay = self.get_death_rate() + self.get_emigration_rate()
        if growth < decay:  # Can't decay more than 3% of population an hour
            return int(max(growth - decay, -0.03 * self.population))
        return growth - decay

    def update_population(self):
        deaths = self.get_death_rate()
        emigration = self.get_emigration_rate()
        births = self.birth_rate
        immigration = self.immigration_rate
        self.population += (births + immigration) - (deaths + emigration)

    # Resources
    def get_tax_income(self):
        return int(self.population * (self.tax_rate / 100))

    def get_upkeep_costs(self):
        return sum(unit.upkeep * unit.total for unit in self.armies.values()) // 24

    def get_wood_income(self):
        return self.buildings['mill'].total * self.buildings['mill'].output

    def get_stone_income(self):
        return self.buildings['quarry'].total * self.buildings['quarry'].output

    def get_excess_production_value(self, value=-1):
        """
        Users the excess production towards completing a task
        """
        economy = self.economy
        if value == -1:
            excess_worker_choice = self.production_choice
        else:
            excess_worker_choice = value

        if excess_worker_choice == self.GOLD:
            return economy.excess_production // 10
        elif excess_worker_choice == self.LAND:
            return economy.excess_production
        elif excess_worker_choice == self.FOOD:
            return economy.excess_production
        elif excess_worker_choice == self.HAPPINESS:
            return 2

    def apply_excess_production_value(self):
        if self.production_choice == 0:
            self.gold += self.get_excess_production_value()
        if self.production_choice == 1:
            self.preferences.produce_land += self.get_excess_production_value()
            # Every 1000 production towards land gives you one acre
            while self.preferences.produce_land >= self.land * 5:
                self.preferences.produce_land -= self.land * 5
                self.land += 1
        if self.production_choice == 2:
            self.grain_stores += self.get_excess_production_value()
        if self.production_choice == 3:
            pass  # Already handled in self.happiness_change

    def produce_pending_buildings(self):
        """
        Gets a list of all buildings which can be built today. Builds it. Then recalls function.
        """
        buildings_to_be_built = self.build_slots
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
    def get_offensive_strength(self, army=None, scoreboard=False, enemy_forts=0):
        """You can use this if you want strength of an army.

        If you just want the entire county strength use
        `county.offensive_power` instead.
        """

        warnings.warn(
            "This might be depreciated in favour of offensive_power attribute, or if you want to pass args Military.offensive_power.fget(county.military, someargs, somekwargs)",
            DeprecationWarning
        )
        military = self.military
        military_cls = military.__class__
        return military_cls.offensive_power.fget(military, army=army, scoreboard=scoreboard, enemy_forts=enemy_forts)

    def get_defensive_strength(self, scoreboard=False):
        # First get base strength of citizens
        local_md = md['metadata']
        modifier = 1 + extract_modifiers(
            local_md.defense_per_citizen_modifier,
            self.race,
            self.background
        )
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

    def remove_casualties_after_attacking(self, attack_power, army, expedition_id):
        casualties = 0
        expedition = Expedition.query.get(expedition_id)
        hit_points_lost = randint(attack_power // 5, attack_power // 4)
        for unit in army.keys():
            setattr(expedition, unit + '_sent', army[unit])
        while hit_points_lost > 0:
            army = {key: value for key, value in army.items() if value > 0}  # Remove dead troops
            if army == {}:
                break
            unit = choice(list(army))
            hit_points_lost -= self.armies[unit].health
            self.armies[unit].total -= 1
            army[unit] -= 1
            casualties += 1
        for unit in army.keys():
            self.armies[unit].traveling += army[unit]  # Surviving troops are marked as absent
            setattr(expedition, unit, army[unit])
        return casualties

    def remove_casualties_after_being_attacked(self, attack_power):
        casualties = 0
        hit_points_lost = randint(attack_power // 8, attack_power // 7)
        hit_points_to_be_removed = hit_points_lost
        for unit in self.armies.values():
            available = unit.available
            if available > 0:
                available_hit_points = available * unit.health
                this_units_damage = min(available_hit_points, hit_points_lost // 4)
                hit_points_to_be_removed -= this_units_damage
                this_dead = this_units_damage // unit.health
                unit.total -= this_dead
                casualties += this_dead
        citizens_killed = min(hit_points_to_be_removed, self.population)
        self.population -= citizens_killed
        return casualties + citizens_killed

    def get_score_from_winning_battle(self, enemy, modifier):
        score = (enemy.land ** 3) / (self.land ** 2) * 0.1
        if self.day > enemy.day:
            modifier -= max((self.day - enemy.day) ** 0.8 / 100, 0)
        score = max(score, 1) * modifier  # Add the current modifier
        score = int(min(score, enemy.land * 0.2))  # Make sure it doesn't exceed 20% of their land
        return score

    def get_resources_from_winning_pillage(self, enemy, modifier):
        enemy_resources = {'gold': (enemy.gold, 1),
                           'wood': (enemy.wood, 1.5),
                           'iron': (enemy.iron, 3)}
        if self.day - enemy.day > 0 and self.land > enemy.land:  # If you are older and larger, we lessen your rewards
            modifier -= (self.day + self.land - enemy.day - enemy.land) ** 0.8 / 100
        enemy_total_value = enemy_resources['gold'][0] + enemy_resources['wood'][0] + enemy_resources['iron'][0]
        attackers_gain_value = min(enemy_total_value * 0.2 * modifier,
                                   500)  # You can gain a maximum of 500 value from a pillage
        gains = {'gold': 0, 'wood': 0, 'iron': 0}
        while attackers_gain_value > 0:
            enemy_resources = {key: value for key, value in enemy_resources.items() if value[0] > 0}
            element = choice(list(enemy_resources))
            attackers_gain_value -= enemy_resources[element][1]
            gains[element] += 1
        return gains

    def battle_results(self, army, enemy, attack_type):
        kingdom = self.kingdom
        enemy_kingdom = enemy.kingdom
        military = self.military
        rewards_modifier = 1.00
        offence_damage = self.get_offensive_strength(army=army, enemy_forts=enemy.buildings["fort"].total)
        defence_damage = enemy.get_defensive_strength()
        expedition = Expedition(self.id, enemy.id, self.kingdom.world.day, self.day, offence_damage, defence_damage,
                                attack_type)
        expedition.save()

        war = kingdom.at_war_with(enemy_kingdom)
        if war:  # If this is true, we are at war with them
            expedition.war_id = war.id
            rewards_modifier += 0.15
        difference_in_power = abs(offence_damage - defence_damage) / ((offence_damage + defence_damage) / 2) * 100
        if offence_damage > defence_damage:
            win = True
        else:
            win = False
        if difference_in_power < 25:
            if win:
                notification_title = f"You were attacked by {self.name} and lost a closely matched battle."
                message = "You won a closely matched battle."
            else:
                notification_title = f"You were attacked by {self.name} but drove them off after a closely matched battle."
                message = "You lost a closely matched battle."
        elif difference_in_power < 50:
            offence_damage *= 0.50
            defence_damage *= 0.50
            if win:
                notification_title = f"You were attacked by {self.name} and lost a resounding defeat."
                message = "You won a resounding victory."
            else:
                notification_title = f"You were attacked by {self.name} but easily defeated them."
                message = "You were resoundingly defeated."
        else:
            offence_damage *= 0.25
            defence_damage *= 0.25
            if win:
                notification_title = f"You were attacked by {self.name} and quickly retreated before suffering many losses."
                message = "The enemy quickly retreated before you."
            else:
                notification_title = f"An army from {self.name} attacked you, but they quickly retreated after seeing your forces."
                message = "Your army quickly retreated from battle."

        buffer_time = datetime.utcnow() - timedelta(hours=12)
        previous_attacks_on_this_county = Expedition.query.filter_by(target_id=enemy.id) \
            .filter_by(success=True) \
            .filter(Expedition.time_created > buffer_time) \
            .count()
        rewards_modifier -= previous_attacks_on_this_county * 0.15
        rewards_modifier = max(0.05, rewards_modifier)

        casualties = self.remove_casualties_after_attacking(defence_damage, army, expedition.id)
        defence_casualties = enemy.remove_casualties_after_being_attacked(attack_power=offence_damage)
        expedition.duration = military.get_expedition_duration(attack_type, win)

        if expedition.monster_sent > 0:
            # Before removing casualties, check for monster impacts
            monster_title = None
            if self.armies['monster'].class_name == 'manticore':
                happiness_impact = expedition.monster_sent * 3
                enemy.happiness -= happiness_impact
                monster_title = "Manticores attack"
                monster_content = f"Your county loses {happiness_impact} " \
                    f"happiness from the panic surrounding the battle."
                message += f" Your manticores terrify the enemy with their shrieks" \
                    f" and cause -{happiness_impact} happiness to their county."

            elif self.armies['monster'].class_name == 'mammoth':
                enemy.destroy_buildings(enemy, expedition.monster_sent, destroy_all=True)
                monster_title = "Mammoths attack"
                monster_content = f"Your county lost {expedition.monster_sent} " \
                    f"buildings from the charging mammoths."
                message += f" Your mammoths stampede the enemy and destroy an additional" \
                    f" {expedition.monster_sent} buildings."

            elif self.armies['monster'].class_name == 'phoenix':
                dead_phoenixes = expedition.monster_sent - expedition.monster
                revived = 0
                for i in range(dead_phoenixes):
                    if randint(0, 1) == 1:
                        revived += 1
                expedition.monster += revived
                casualties -= revived
                message += f" Miraculously, {revived} of your Phoenixes were reborn after the battle " \
                    f"and rejoin your army."

            elif self.armies['monster'].class_name == 'wyvern':
                noxious_fumes = Casting(self.id, enemy.id, None, self.kingdom.world.day, self.day, "noxious_fumes",
                                        "Noxious Fumes", expedition.monster_sent, "Hostile")
                noxious_fumes.save()
                monster_title = "Wyverns attack"
                monster_content = f"The noxious fumes from the wyvern's attack has engulfed our lands" \
                    f" and will persist for {expedition.monster_sent} days."
                message += f" Your wyverns shroud the enemy county in noxious fumes" \
                    f" which should last for {expedition.monster_sent} days."

            if monster_title:
                notification = Notification(enemy, monster_title, monster_content)
                notification.save()

        if win:
            expedition.success = True
            war_score = self.get_score_from_winning_battle(enemy, rewards_modifier)
            if expedition.mission == "Attack":
                expedition.land_acquired = war_score
                enemy.land -= war_score
                notification = Notification(
                    enemy,
                    notification_title,
                    f"You lost {war_score} acres and {defence_casualties} troops in the battle.",
                )
                message += f" You gained {war_score} acres, but lost {casualties} troops in the battle."
            elif expedition.mission == "Raze":
                land_razed = int(war_score * 1.40)
                expedition.land_razed = land_razed
                enemy.land -= land_razed
                notification = Notification(
                    enemy,
                    notification_title,
                    f"The enemy razed {land_razed} acres and {defence_casualties} troops in the battle.",
                )
                message += f" You razed {land_razed} acres, but lost {casualties} troops in the battle."
            elif expedition.mission == "Pillage":
                gains = self.get_resources_from_winning_pillage(enemy, rewards_modifier)
                expedition.gold_gained = gains['gold']
                expedition.wood_gained = gains['wood']
                expedition.iron_gained = gains['iron']
                self.gold += gains['gold']
                self.wood += gains['wood']
                self.iron += gains['iron']
                enemy.gold -= gains['gold']
                enemy.wood -= gains['wood']
                enemy.iron -= gains['iron']
                notification = Notification(
                    enemy,
                    notification_title,
                    f"The enemy army stole {gains['gold']} gold, {gains['wood']} wood, "
                    f"and {gains['iron']} iron after the battle.",
                )
                message += f" You gained {gains['gold']} gold, {gains['wood']} wood, " \
                    f"and {gains['iron']} iron, but lost {casualties} troops in the battle."
            # Add war clause since it was a successful attack
            # TODO: defender should gain points as well.
            kingdom.distribute_war_points(enemy_kingdom, war_score)
        else:
            enemy_kingdom.distribute_war_points(kingdom, casualties // 10)
            expedition.success = False
            notification = Notification(
                enemy,
                notification_title,
                f"You achieved a victory but lost {defence_casualties} troops.",
            )
        message += f" You lost {casualties} troops in the battle."
        notification.category = "Military"
        notification.save()

        return message, offence_damage

    @staticmethod
    def destroy_buildings(county, land_destroyed, destroy_all=False):
        # destroy_all means it will always destroy this amount if you have it. Otherwise the amount destroyed is random.
        if destroy_all:
            destroyed = 0
        else:
            destroyed = randint(0, county.get_available_land())  # The more available land, the less likely building are destroyed
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

    # Achievements
    def check_incremental_achievement(self, name, amount):
        # Currently this does nothing but it's here for flexibility.
        self.user.check_incremental_achievement(name, amount)

    def display_news(self):
        events = Notification.query.filter_by(county_id=self.id, new=True).order_by(
            Notification.time_created.desc()).all()
        for event in events:
            event.new = False
        return events

    def display_old_news(self):
        events = Notification.query.filter_by(county_id=self.id, new=False).order_by(
            Notification.time_created.desc()).all()
        return events

    # Infiltrations
    def get_number_of_available_thieves(self):
        all_current_missions = Infiltration.query.filter_by(county_id=self.id).filter(Infiltration.duration > 0).all()
        unavailable_thieves = sum(mission.amount_of_thieves for mission in all_current_missions)
        return self.thief_slots - unavailable_thieves

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

    def get_chance_to_catch_enemy_thieves(self):
        buffer_time = datetime.utcnow() - timedelta(hours=12)
        operations_on_target = Infiltration.query.filter_by(target_id=self.id).filter_by(success=True).filter(
            Infiltration.time_created > buffer_time).all()
        chance = 0
        for mission in operations_on_target:  # Each thief who invaded you gives you some protection
            chance += (mission.amount_of_thieves * 5)

        chance += (self.buildings['tower'].total ** 0.8) * 100 / self.land * self.buildings['tower'].output

        modify_thief_prevention = Casting.query.filter_by(target_id=self.id, name="modify_thief_prevention").filter(
            (Casting.duration > 0) | (Casting.active == True)).all()
        for spell in modify_thief_prevention or []:
            chance += spell.output * self.spell_modifier

        return get_int_between_0_and_100(chance)

    def chance_to_disrupt_spell(self):
        chance = 0

        modify_magic_disrupt = Casting.query.filter_by(target_id=self.id, name="modify_magic_disrupt").filter(
            (Casting.duration > 0) | (Casting.active == True)).all()
        for spell in modify_magic_disrupt or []:
            chance += spell.output * self.spell_modifier

        if self.race == "Dwarf":
            chance += 15

        return get_int_between_0_and_100(chance)

    # Terminology
    @property
    def healthiness_terminology(self):
        if self.healthiness < 20:
            return "dying of disease and hunger"
        if self.healthiness < 50:
            return "sick and starving"
        if self.healthiness < 75:
            return "hungry"
        if self.healthiness < 90:
            return "healthy"
        return "perfect health"

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
        terminology_dictionary = {0: "None", 0.25: "Quarter", 0.5: "Half", 0.75: "Three Quarters",
                                  1: "Normal", 1.5: "One-and-a-half", 2: "Double", 3: "Triple"}
        return terminology_dictionary[self.rations]

    def __repr__(self):
        return '<County %r (%r)>' % (self.name, self.id)
