from datetime import datetime, timedelta
from random import choice, randint

from sqlalchemy import desc
from sqlalchemy.orm.collections import attribute_mapped_collection

from undyingkingdoms.models.bases import GameState, db
from undyingkingdoms.models.helpers import cached_random
from undyingkingdoms.models.notifications import Notification
from undyingkingdoms.models.expeditions import Expedition
from undyingkingdoms.models.infiltrations import Infiltration
from undyingkingdoms.models.technologies import Technology
from undyingkingdoms.models.trades import Trade
from undyingkingdoms.models.magic import Casting
from undyingkingdoms.static.metadata.armies.metadata_armies_updater import update_armies
from undyingkingdoms.static.metadata.magic.metadata_magic_artificer import artificer_spells
from undyingkingdoms.static.metadata.magic.metadata_magic_cleric import cleric_spells
from undyingkingdoms.static.metadata.magic.metadata_magic_diplomat import diplomat_spells
from undyingkingdoms.static.metadata.magic.metadata_magic_druid import druid_spells
from undyingkingdoms.static.metadata.magic.metadata_magic_hierophant import hierophant_spells
from undyingkingdoms.static.metadata.metadata import birth_rate_modifier, food_consumed_modifier, death_rate_modifier, \
    income_modifier, production_per_worker_modifier, offensive_power_modifier, defense_per_citizen_modifier, \
    happiness_modifier, buildings_produced_per_day, food_produced_modifier

from copy import deepcopy

from undyingkingdoms.static.metadata.armies.metadata_armies_dwarf import dwarf_armies
from undyingkingdoms.static.metadata.armies.metadata_armies_elf import elf_armies
from undyingkingdoms.static.metadata.armies.metadata_armies_goblin import goblin_armies
from undyingkingdoms.static.metadata.armies.metadata_armies_human import human_armies
from undyingkingdoms.static.metadata.armies.metadata_armies_ogre import ogre_armies
from undyingkingdoms.static.metadata.buildings.metadata_buildings_dwarf import dwarf_buildings
from undyingkingdoms.static.metadata.buildings.metadata_buildings_elf import elf_buildings
from undyingkingdoms.static.metadata.buildings.metadata_buildings_goblin import goblin_buildings
from undyingkingdoms.static.metadata.buildings.metadata_buildings_human import human_buildings
from undyingkingdoms.static.metadata.buildings.metadata_buildings_ogre import ogre_buildings
from undyingkingdoms.static.metadata.magic.metadata_magic_alchemist import alchemist_spells
from undyingkingdoms.static.metadata.magic.metadata_magic_all import generic_spells
from undyingkingdoms.static.metadata.magic.metadata_magic_dwarf import dwarf_spells
from undyingkingdoms.static.metadata.magic.metadata_magic_elf import elf_spells
from undyingkingdoms.static.metadata.magic.metadata_magic_goblin import goblin_spells
from undyingkingdoms.static.metadata.magic.metadata_magic_human import human_spells
from undyingkingdoms.static.metadata.magic.metadata_magic_merchant import merchant_spells
from undyingkingdoms.static.metadata.magic.metadata_magic_ogre import ogre_spells
from undyingkingdoms.static.metadata.magic.metadata_magic_rogue import rogue_spells
from undyingkingdoms.static.metadata.magic.metadata_magic_warlord import warlord_spells
from undyingkingdoms.static.metadata.magic.metadata_magic_wizard import wizard_spells
from undyingkingdoms.static.metadata.research.metadata_research_alchemist import alchemist_technology
from undyingkingdoms.static.metadata.research.metadata_research_all import generic_technology
from undyingkingdoms.static.metadata.research.metadata_research_artificer import artificer_technology
from undyingkingdoms.static.metadata.research.metadata_research_cleric import cleric_technology
from undyingkingdoms.static.metadata.research.metadata_research_diplomat import diplomat_technology
from undyingkingdoms.static.metadata.research.metadata_research_druid import druid_technology
from undyingkingdoms.static.metadata.research.metadata_research_dwarf import dwarf_technology
from undyingkingdoms.static.metadata.research.metadata_research_elf import elf_technology
from undyingkingdoms.static.metadata.research.metadata_research_goblin import goblin_technology
from undyingkingdoms.static.metadata.research.metadata_research_hierophant import hierophant_technology
from undyingkingdoms.static.metadata.research.metadata_research_human import human_technology
from undyingkingdoms.static.metadata.research.metadata_research_merchant import merchant_technology
from undyingkingdoms.static.metadata.research.metadata_research_ogre import ogre_technology
from undyingkingdoms.static.metadata.research.metadata_research_rogue import rogue_technology
from undyingkingdoms.static.metadata.research.metadata_research_warlord import warlord_technology
from undyingkingdoms.static.metadata.research.metadata_research_wizard import wizard_technology


class County(GameState):
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

    buildings = db.relationship("Building",
                                collection_class=attribute_mapped_collection('name'),
                                cascade="all, delete, delete-orphan", passive_deletes=True)
    armies = db.relationship("Army",
                             collection_class=attribute_mapped_collection('name'),
                             cascade="all, delete, delete-orphan", passive_deletes=True)
    technologies = db.relationship("Technology",
                                   collection_class=attribute_mapped_collection('name'),
                                   cascade="all, delete, delete-orphan", passive_deletes=True)
    magic = db.relationship("Magic",
                            collection_class=attribute_mapped_collection('name'),
                            cascade="all, delete, delete-orphan", passive_deletes=True)

    preferences = db.relationship("Preferences", uselist=False)

    def __init__(self, kingdom_id, name, leader, user_id, race, title, background):
        self.name = name
        self.leader = leader
        self.user_id = user_id
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
        # Buildings and Armies extracted from metadata
        if self.race == 'Dwarf':
            self.buildings = deepcopy(dwarf_buildings)
            self.armies = deepcopy(dwarf_armies)
            self.magic = {**deepcopy(generic_spells), **deepcopy(dwarf_spells)}
            self.technologies = {**deepcopy(generic_technology), **deepcopy(dwarf_technology)}
        elif self.race == 'Human':
            self.buildings = deepcopy(human_buildings)
            self.armies = deepcopy(human_armies)
            self.magic = {**deepcopy(generic_spells), **deepcopy(human_spells)}
            self.technologies = {**deepcopy(generic_technology), **deepcopy(human_technology)}
        elif self.race == 'Elf':
            self.buildings = deepcopy(elf_buildings)
            self.armies = deepcopy(elf_armies)
            self.magic = {**deepcopy(generic_spells), **deepcopy(elf_spells)}
            self.technologies = {**deepcopy(generic_technology), **deepcopy(elf_technology)}
        elif self.race == 'Goblin':
            self.buildings = deepcopy(goblin_buildings)
            self.armies = deepcopy(goblin_armies)
            self.magic = {**deepcopy(generic_spells), **deepcopy(goblin_spells)}
            self.technologies = {**deepcopy(generic_technology), **deepcopy(goblin_technology)}
        elif self.race == 'Ogre':
            self.buildings = deepcopy(ogre_buildings)
            self.armies = deepcopy(ogre_armies)
            self.magic = {**deepcopy(generic_spells), **deepcopy(ogre_spells)}
            self.technologies = {**deepcopy(generic_technology), **deepcopy(ogre_technology)}
        else:
            raise AttributeError('Buildings and Armies were not found in metadata')

        self.armies = update_armies(self.background, self.armies)

        if self.background == "Alchemist":
            self.magic = {**self.magic, **deepcopy(alchemist_spells)}
            self.technologies = {**self.technologies, **deepcopy(alchemist_technology)}
            self.buildings["lab"].output *= 2

        elif self.background == "Artificer":
            self.magic = {**self.magic, **deepcopy(artificer_spells)}
            self.technologies = {**self.technologies, **deepcopy(artificer_technology)}

        elif self.background == "Cleric":
            self.magic = {**self.magic, **deepcopy(cleric_spells)}
            self.technologies = {**self.technologies, **deepcopy(cleric_technology)}

        elif self.background == "Diplomat":
            self.magic = {**self.magic, **deepcopy(diplomat_spells)}
            self.technologies = {**self.technologies, **deepcopy(diplomat_technology)}

        elif self.background == "Druid":
            self.magic = {**self.magic, **deepcopy(druid_spells)}
            self.technologies = {**self.technologies, **deepcopy(druid_technology)}

        elif self.background == "Hierophant":
            self.magic = {**self.magic, **deepcopy(hierophant_spells)}
            self.technologies = {**self.technologies, **deepcopy(hierophant_technology)}

        elif self.background == "Merchant":
            self.magic = {**self.magic, **deepcopy(merchant_spells)}
            self.technologies = {**self.technologies, **deepcopy(merchant_technology)}

        elif self.background == "Warlord":
            self.magic = {**self.magic, **deepcopy(warlord_spells)}
            self.technologies = {**self.technologies, **deepcopy(warlord_technology)}

        elif self.background == "Wizard":
            self.magic = {**self.magic, **deepcopy(wizard_spells)}
            self.technologies = {**self.technologies, **deepcopy(wizard_technology)}

        elif self.background == "Rogue":
            self.magic = {**self.magic, **deepcopy(rogue_spells)}
            self.technologies = {**self.technologies, **deepcopy(rogue_technology)}

    def get_int_between_0_to_100(self, input):
        return int(max(min(100, input), 0))

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
        self._happiness = self.get_int_between_0_to_100(value)

    @property
    def healthiness(self):
        return self._healthiness

    @healthiness.setter
    def healthiness(self, value):
        self._healthiness = self.get_int_between_0_to_100(value)

    @property
    def tax_rate(self):
        return self.preferences.tax_rate

    @tax_rate.setter
    def tax_rate(self, value):
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
    def production_choice(self, value):
        self.preferences.production_choice = value

    @property
    def research_choice(self):
        return self.preferences.research_choice

    @research_choice.setter
    def research_choice(self, value):
        self.preferences.research_choice = value

    @property
    def max_mana(self):
        base = 40
        if self.technologies['arcane knowledge I'].completed:
            base += 20
        if self.technologies['arcane knowledge II'].completed:
            base += 20
        if self.technologies['arcane knowledge III'].completed:
            base += 20
        return base

    @property
    def spell_modifier(self):
        return 1 + (self.buildings["arcane"].total * self.buildings["arcane"].output / 100)

    @property
    def seed(self):
        return self.kingdom.world.day

    # Voting
    def can_vote(self):
        if self.preferences.last_vote_date and datetime.utcnow() > (self.preferences.last_vote_date - timedelta(hours=24)):
            return False
        else:
            return True

    def cast_vote(self, vote):
        self.preferences.vote = vote
        self.preferences.last_vote_date = datetime.utcnow()
        self.kingdom.count_votes()

    def display_vote(self):
        vote = County.query.get(self.preferences.vote)
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
                notification = Notification(self.id,
                                            "Your army has returned",
                                            "Error: Report to admin",
                                            self.kingdom.world.day,
                                            "Military")
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
                target_county = County.query.get(trade.target_id)
                notification = Notification(self.id, "Trade Offer",
                                            f"Your trade offer to {target_county.name} has expired and your resources have been return", self.kingdom.world.day, "Trade")
                notification.save()
        infiltrations = Infiltration.query.filter_by(county_id=self.id).filter(Infiltration.duration > 0).all()
        for infiltration in infiltrations:
            infiltration.duration -= 1
            if infiltration.duration == 0:
                notification = Notification(self.id,
                                            "Your thieves have returned",
                                            "Error: Report to admin",
                                            self.kingdom.world.day,
                                            "Thieves")
                notification.save()
                notification.content = f"Your {infiltration.amount_of_thieves} thieves have returned after their mission to {infiltration.mission}."

        spells = Casting.query.filter_by(target_id=self.id).filter(Casting.duration > 0).all()
        for spell in spells:
            spell.duration -= 1
            if spell.duration == 0:
                notification = Notification(self.id,
                                            "A spell has ended",
                                            "Error: Report to admin",
                                            self.kingdom.world.day,
                                            "Magic")
                notification.save()
                notification.content = f"{spell.name} has ended and is no longer affecting your county."

        self.day += 1

    def temporary_bot_tweaks(self):
        from undyingkingdoms.models.users import User

        friendly_counties = County.query.join(User).filter(County.kingdom_id==self.kingdom_id, ~User.is_bot).all()
        friendly_counties_ids = [county.id for county in friendly_counties]
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
        if randint(1, 24) == 24 and self.kingdom.leader == 0 and friendly_counties_ids:
            self.cast_vote(choice(friendly_counties_ids))
        if randint(1, 10) == 10 and self.get_available_land() >= 5:
            self.buildings['house'].total += 3
            self.buildings['field'].total += 1
            self.buildings['pasture'].total += 1
        if randint(1, 12) == 12:
            trading_partner = choice(friendly_counties_ids)
            trade_notice = Notification(trading_partner,
                                        "You were offered a trade", f"{self.name} has offered you a trade. Visit the trading page.",
                                        self.kingdom.world.day, "Trade")
            trade_notice.save()
            random = randint(1, 5)
            if random == 1:  # Send wood for gold
                trade_offered = Trade(self.id, trading_partner, self.kingdom.world.day, 24, 0, 40, 0, 0, 0, 60, 0, 0, 0, 0)
                self.wood -= 40
            if random == 2:  # Send iron for gold
                trade_offered = Trade(self.id, trading_partner, self.kingdom.world.day, 24, 0, 0, 30, 0, 0, 90, 0, 0, 0, 0)
                self.iron -= 30
            if random == 3:  # Send gold for iron and wood
                trade_offered = Trade(self.id, trading_partner, self.kingdom.world.day, 24, 120, 0, 0, 0, 0, 0, 40, 20, 0, 0)
                self.gold -= 120
            if random == 4:  # Send food for wood
                trade_offered = Trade(self.id, trading_partner, self.kingdom.world.day, 24, 0, 0, 0, 0, 750, 0, 0, 0, 0, 50)
                self.gold -= 120
            if random == 5:  # Send food for iron
                trade_offered = Trade(self.id, trading_partner, self.kingdom.world.day, 24, 0, 0, 0, 0, 750, 0, 40, 20, 0, 0)
                self.gold -= 120
            trade_offered.save()

    def update_daily_resources(self):
        self.gold += self.get_gold_change()
        self.wood += self.get_wood_income()
        self.iron += self.get_iron_income()
        self.stone += self.get_stone_income()
        self.mana += self.get_mana_change()
        self.research += self.get_research_change()
        self.happiness += self.get_happiness_change()

    def advance_research(self):
        technology = self.technologies[self.research_choice]
        technology.current += self.research
        if technology.current >= technology.required:  # You save left over research
            self.research = technology.current - technology.required
            technology.completed = True
            available_technologies = self.get_available_technologies()
            if available_technologies:
                self.research_choice = available_technologies[0].name
            else:
                self.research = 0
        else:
            self.research = 0
            
    def get_available_technologies(self):
        available_technologies = Technology.query.filter_by(county_id=self.id).filter_by(completed=False).filter_by(tier=1).all()
        if not available_technologies:
            available_technologies = Technology.query.filter_by(county_id=self.id).filter_by(completed=False).filter_by(tier=2).all()
        if not available_technologies:
            available_technologies = Technology.query.filter_by(county_id=self.id).filter_by(completed=False).filter_by(tier=3).all()
        return available_technologies

    def get_happiness_change(self):
        change = 7 - self.tax_rate
        if self.production_choice == 3:
            change += self.get_excess_production_value(self.production_choice)
        modifier = happiness_modifier.get(self.race, ("", 0))[1] + happiness_modifier.get(self.background, ("", 0))[1]
        if self.technologies['public works'].completed:
            modifier += 1
        return change + modifier

    def update_weather(self):
        self.preferences.weather = choice(self.preferences.weather_choices)

    def get_random_daily_events(self):
        self.preferences.days_since_event += 1
        random_chance = randint(0, self.preferences.days_since_event)
        if random_chance < 15:
            return
        random_chance = randint(1, 8)
        notification = None
        if random_chance == 1 and self.grain_stores > 0:
            amount = int(randint(3, 7) * self.grain_stores / 100)
            notification = Notification(self.id,
                                        "Rats have gotten into your grain silos",
                                        f"Your county lost {amount} of its stored grain.",
                                        self.kingdom.world.day)
            self.grain_stores -= amount

        elif random_chance == 2 and self.happiness > 90:
            amount = randint(100, 200)
            notification = Notification(self.id,
                                        "Your people celebrate your rule",
                                        f"Your people hold a feast and offer you {amount} gold as tribute.",
                                        self.kingdom.world.day)
            self.gold += amount

        elif random_chance == 3 and self.buildings['pasture'].total > 0:
            amount = min(randint(2, 4), self.buildings['pasture'].total)
            notification = Notification(self.id,
                                        "A disease has affected your cattle",
                                        f"Your county has lost {amount} of its dairy farms.",
                                        self.kingdom.world.day)
            self.buildings['pasture'].total -= amount

        elif random_chance == 4 and self.buildings['field'].total > 0:
            amount = min(randint(1, 3), self.buildings['field'].total)
            notification = Notification(self.id,
                                        "Storms have ravaged your crops",
                                        f"A massive storm has destroyed {amount} of your fields.",
                                        self.kingdom.world.day)
            self.buildings['field'].total -= amount
            self.preferences.weather = 'thunderstorm'

        elif random_chance == 5 and self.buildings['field'].total > 0:
            amount = self.buildings['field'].total * 15
            notification = Notification(self.id,
                                        "Booster crops",
                                        f"Due to excellent weather this season, your crops produced an addition {amount} grain today.",
                                        self.kingdom.world.day)
            self.grain_stores += amount
            self.preferences.weather = 'lovely'

        elif random_chance == 6:
            modifier = ((101 - self.healthiness) // 20 + 3) / 100  # Percent of people who will die (1% -> 5%)
            amount = int(modifier * self.population)
            notification = Notification(self.id,
                                        "Black Death",
                                        f"A plague has swept over our county, killing {amount} of our people.",
                                        self.kingdom.world.day)
            self.population -= amount

        elif random_chance == 7 and self.buildings['house'].total > 0:
            amount = min(randint(2, 4), self.buildings['house'].total)
            notification = Notification(self.id,
                                        "Disaster",
                                        f"A fire has spread in the city burning down {amount} of your {self.buildings['house'].class_name}.",
                                        self.kingdom.world.day)
            self.buildings['house'].total -= amount

        if notification:
            notification.category = "Random Event"
            notification.save()
            self.preferences.days_since_event = 0

    def get_healthiness_change(self):
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
        modifier = 1
        modifier += food_produced_modifier.get(self.race, ("", 0))[1] + food_produced_modifier.get(self.background, ("", 0))[1]
        if self.technologies['agriculture'].completed:
            modifier += 0.5
        modify_grain_rate = Casting.query.filter_by(target_id=self.id, name="modify_grain_rate").filter((Casting.duration > 0) | (Casting.active == True)).all()
        for spell in modify_grain_rate or []:
            modifier += spell.output * self.spell_modifier
        return int(self.buildings['field'].total * self.buildings['field'].output * modifier)

    def get_produced_dairy(self):
        modifier = 1
        modifier += food_produced_modifier.get(self.race, ("", 0))[1] + food_produced_modifier.get(self.background, ("", 0))[1]
        if self.technologies['animal husbandry'].completed:
            modifier += 0.5
        verdant_growth = Casting.query.filter_by(target_id=self.id, active=1, name="verdant growth").first()
        if verdant_growth:
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

        modify_death_rate = Casting.query.filter_by(target_id=self.id, name="modify_death_rate").filter(
            (Casting.duration > 0) | (Casting.active == True)).all()
        for spell in modify_death_rate or []:
            modifier += spell.output * self.spell_modifier

        death_rate = (2 / self.healthiness) * modifier

        return int(death_rate * self.population)

    def get_birth_rate(self):
        modifier = 1 + birth_rate_modifier.get(self.race, ("", 0))[1] + \
                   birth_rate_modifier.get(self.background, ("", 0))[1]
        modifier += (self.buildings['house'].total / self.land) * self.buildings['house'].output

        modify_birth_rate = Casting.query.filter_by(target_id=self.id, name="modify_birth_rate").filter((Casting.duration > 0) | (Casting.active == True)).all()
        for spell in modify_birth_rate or []:
            modifier += spell.output * self.spell_modifier

        raw_rate = (self.happiness / 100) * (self.land / 5)  # 5% times your happiness rating
        return int(raw_rate * modifier)

    def get_immigration_rate(self):
        random_hash = (self.kingdom.world.day ** 2) % 10
        return 25 + random_hash

    def get_emigration_rate(self):
        return int((self.preferences.tax_rate * 3) + self.kingdom.world.age + (0.005 * self.population))

    @cached_random
    def get_population_change(self):
        growth = self.get_birth_rate() + self.get_immigration_rate()
        decay = self.get_death_rate() + self.get_emigration_rate()
        if growth < decay:  # Can't decay more than 3% of population an hour
            return int(max(growth - decay, -0.03 * self.population))
        return growth - decay

    def update_population(self):
        deaths = self.get_death_rate()
        emigration = self.get_emigration_rate()
        births = self.get_birth_rate()
        immigration = self.get_immigration_rate()
        self.population += (births + immigration) - (deaths + emigration)

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
        if self.technologies.get("economics") and self.technologies["economics"].completed:
            modifier += 0.15
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
        if self.technologies.get("smelting") and self.technologies["smelting"].completed:
            return self.buildings['mine'].total * (self.buildings['mine'].output + 1)
        return self.buildings['mine'].total * self.buildings['mine'].output

    def get_stone_income(self):
        return self.buildings['quarry'].total * self.buildings['quarry'].output

    def get_mana_change(self):
        growth = 2
        active_spells = Casting.query.filter_by(county_id=self.id).filter_by(active=True).all()
        loss = sum(spell.mana_sustain for spell in active_spells)
        difference = growth - loss
        if difference < 0 and self.mana + difference < 0:
            active_spells[0].active = False
            notice = Notification(self.id,
                                  "Spell Ended",
                                  f"You did not have enough mana and {active_spells[0].name} ended.",
                                  self.kingdom.world.day,
                                  "Spell End")
            notice.save()
            return self.get_mana_change()
        return difference

    def get_research_change(self):
        if self.technologies.get("arcane knowledge") and self.technologies["arcane knowledge"].completed:
            return self.buildings['lab'].total * (self.buildings['lab'].output + 1)
        return self.buildings['lab'].total * self.buildings['lab'].output

    # Building
    def get_production_modifier(self):  # Modifiers your excess production
        return 1 + production_per_worker_modifier.get(self.race, ("", 0))[1] \
               + production_per_worker_modifier.get(self.background, ("", 0))[1]

    def get_excess_production(self):
        """
        Returns the amount of excess production you get each turn
        """
        if self.technologies.get("slavery")  and self.technologies["slavery"].completed:
            return max(int(self.get_production_modifier() * self.get_available_workers() * 2), 0)
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
            return self.get_excess_production() // 10
        if excess_worker_choice == 1:  # Land
            return self.get_excess_production()
        if excess_worker_choice == 2:  # Food
            return self.get_excess_production()
        if excess_worker_choice == 3:  # Happiness
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
            pass  # Already handled in self.get_happiness_change()

    def get_number_of_buildings_produced_per_day(self):
        amount = 3

        if self.technologies.get("engineering") and self.technologies["engineering"].completed:
            amount += 1

        amount += buildings_produced_per_day.get(self.race, ("", 0))[1] \
                  + buildings_produced_per_day.get(self.background, ("", 0))[1]

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
        if army is None and county is None:
            county = self
        strength = 0
        modifier = 1 + offensive_power_modifier.get(self.race, ("", 0))[1] \
                   + offensive_power_modifier.get(self.background, ("", 0))[1]

        if self.technologies['steel'].completed:
            modifier += 0.10

        modify_offensive_power = Casting.query.filter_by(target_id=self.id, name="modify_offensive_power").filter((Casting.duration > 0) | (Casting.active == True)).all()
        for spell in modify_offensive_power or []:
            modifier += spell.output * self.spell_modifier

        if army:
            for unit in self.armies.values():
                if unit.name != 'archer' and unit.name != 'besieger':
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

    def get_army_duration(self, win, attack_type):
        base_duration = {'Attack': 18, 'Pillage': 12, 'Raze': 8}
        speed_reduction = 100
        speed_reduction += self.buildings['stables'].total * self.buildings['stables'].output
        duration = base_duration[attack_type] * 100 / speed_reduction
        if self.technologies["logistics"].completed:
            duration -= 1
        if win is False:
            duration *= 0.5
        return int(max(duration, 3))

    def remove_casualties_after_attacking(self, attack_power, army, expedition_id):
        casualties = 0
        expedition = Expedition.query.get(expedition_id)
        hit_points_lost = randint(attack_power // 8, attack_power // 7)
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

    def battle_results(self, army, enemy, attack_type):
        war = None
        rewards_modifier = 1.00
        offence_damage = self.get_offensive_strength(army=army)
        defence_damage = enemy.get_defensive_strength()
        expedition = Expedition(self.id, enemy.id, self.kingdom.world.day, self.day, offence_damage, defence_damage, attack_type)
        expedition.save()
        for each_war in self.kingdom.wars:
            if each_war.get_other_kingdom(self.kingdom) == enemy.kingdom:  # If this is true, we are at war with them
                war = each_war
                expedition.war_id = war.id
                rewards_modifier += 0.15
                break
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
        previous_attacks_on_this_county = Expedition.query.filter_by(target_id=enemy.id)\
            .filter_by(success=True)\
            .filter(Expedition.time_created > buffer_time)\
            .count()
        rewards_modifier -= previous_attacks_on_this_county * 0.15
        rewards_modifier = max(0.05, rewards_modifier)

        casualties = self.remove_casualties_after_attacking(defence_damage, army, expedition.id)
        defence_casualties = enemy.remove_casualties_after_being_attacked(attack_power=offence_damage)
        expedition.duration = self.get_army_duration(win, attack_type)
        if win:
            expedition.success = True
            if expedition.mission == "Attack":
                land_gained = max((enemy.land ** 3) * 0.1 / (self.land ** 2), 1) * rewards_modifier
                land_gained = int(min(land_gained, enemy.land * 0.2))
                war_score = land_gained
                expedition.land_acquired = land_gained
                enemy.land -= land_gained
                notification = Notification(enemy.id, notification_title,
                                            f"You lost {land_gained} acres and {defence_casualties} troops in the battle.",
                                            self.kingdom.world.day)
                message += f" You gained {land_gained} acres, but lost {casualties} troops in the battle."
            elif expedition.mission == "Raze":
                land_razed = max((enemy.land ** 3) * 0.1 / (self.land ** 2), 1) * rewards_modifier
                land_razed = int(min(land_razed, enemy.land * 0.2))
                war_score = land_razed
                expedition.land_razed = land_razed
                enemy.land -= land_razed
                notification = Notification(enemy.id, notification_title,
                                            f"The enemy razed {land_razed} acres and {defence_casualties} troops in the battle.",
                                            self.kingdom.world.day)
                message += f" You razed {land_razed} acres, but lost {casualties} troops in the battle."
            elif expedition.mission == "Pillage":
                war_score = int(min(max((enemy.land ** 3) * 0.1 / (self.land ** 2), 1) * rewards_modifier, enemy.land * 0.2))
                enemy_resources = {'gold': (enemy.gold, 1),
                                   'wood': (enemy.wood, 1.5),
                                   'iron': (enemy.iron, 3)}
                enemy_total_value = enemy_resources['gold'][0] + enemy_resources['wood'][0] + enemy_resources['iron'][0]
                attackers_gain_value = min(enemy_total_value * 0.2 * rewards_modifier, 500)  # You can gain a maximum of 500 value from a pillage
                gains = {'gold': 0, 'wood': 0, 'iron': 0}
                while attackers_gain_value > 0:
                    enemy_resources = {key: value for key, value in enemy_resources.items() if value[0] > 0}
                    element = choice(list(enemy_resources))
                    attackers_gain_value -= enemy_resources[element][1]
                    gains[element] += 1
                expedition.gold_gained = gains['gold']
                expedition.wood_gained = gains['wood']
                expedition.iron_gained = gains['iron']
                self.gold += gains['gold']
                self.wood += gains['wood']
                self.iron += gains['iron']
                enemy.gold -= gains['gold']
                enemy.wood -= gains['wood']
                enemy.iron -= gains['iron']
                notification = Notification(enemy.id, notification_title,
                                            f"The enemy army stole {gains['gold']} gold, {gains['wood']} wood, and {gains['iron']} iron after the battle.",
                                            self.kingdom.world.day)
                message += f" You gained {gains['gold']} gold, {gains['wood']} wood, and {gains['iron']} iron, but lost {casualties} troops in the battle."
            # Add war clause since it was a successful attack
            if war:
                if war.kingdom_id == self.kingdom.id:  # We are the attack
                    war.attacker_current += war_score
                    if war.attacker_current >= war.attacker_goal:
                        self.kingdom.war_won(war)
                        war.status = "Won"
                        message += f" We have won the war against {enemy.kingdom.name}!"
                else:
                    war.defender_current += war_score
                    if war.defender_current >= war.defender_goal:
                        enemy.kingdom.war_won(war)
                        war.status = "Lost"
                        message += f" We have won the war against {enemy.kingdom.name}!"
        else:
            expedition.success = False
            notification = Notification(enemy.id, notification_title,
                                        f"You achieved a victory but lost {defence_casualties} troops.",
                                        self.kingdom.world.day)
            message += f" You lost {casualties} troops in the battle."
        notification.category = "Military"
        notification.save()
        return message

    @staticmethod
    def destroy_buildings(county, land_destroyed):
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
        events = Notification.query.filter_by(county_id=self.id, new=True).order_by(Notification.time_created.desc()).all()
        for event in events:
            event.new = False
        return events

    def display_old_news(self):
        events = Notification.query.filter_by(county_id=self.id, new=False).order_by(Notification.time_created.desc()).all()
        return events

    def get_total_number_of_thieves(self):
        base = self.buildings['tavern'].total
        modifier = self.buildings['tavern'].output
        if "espionage i" in self.technologies and self.technologies["espionage i"].completed:
            modifier += 1
        if "espionage ii" in self.technologies and self.technologies["espionage ii"].completed:
            modifier += 1
        if "espionage iii" in self.technologies and self.technologies["espionage iii"].completed:
            modifier += 1
        return base * modifier

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

    def get_chance_to_catch_enemy_thieves(self):
        buffer_time = datetime.utcnow() - timedelta(hours=12)
        operations_on_target = Infiltration.query.filter_by(target_id=self.id).filter_by(success=True).filter(
            Infiltration.time_created > buffer_time).all()
        chance = 0
        for mission in operations_on_target:  # Each thief who invaded you gives you some protection
            chance += (mission.amount_of_thieves * 5)

        chance += self.buildings['tower'].total * self.buildings['tower'].output

        modify_thief_prevention = Casting.query.filter_by(target_id=self.id, name="modify_thief_prevention").filter(
            (Casting.duration > 0) | (Casting.active == True)).all()
        for spell in modify_thief_prevention or []:
            chance += spell.output * self.spell_modifier

        return self.get_int_between_0_to_100(chance)

    def chance_to_disrupt_spell(self):
        chance = 0

        modify_magic_disrupt = Casting.query.filter_by(target_id=self.id, name="modify_magic_disrupt").filter((Casting.duration > 0) | (Casting.active == True)).all()
        for spell in modify_magic_disrupt or []:
            chance += spell.output * self.spell_modifier

        if self.race == "Dwarf":
            chance += 15

        return self.get_int_between_0_to_100(chance)

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


# Attach any add-ons needed to the County class.
from .county_addons.casting_addon import casting_addon

casting_addon(County)
