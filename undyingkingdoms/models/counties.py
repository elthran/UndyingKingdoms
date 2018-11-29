from datetime import datetime, timedelta
from random import choice, uniform, randint

from sqlalchemy.orm.collections import attribute_mapped_collection

# from undyingkingdoms.calculations.counties import get_attack_power
from undyingkingdoms.models.bases import GameState, db
from undyingkingdoms.models.notifications import Notification
from undyingkingdoms.static.metadata import dwarf_armies, human_armies, dwarf_buildings, \
	human_buildings, rations_translations_tables, kingdom_names

from copy import deepcopy


class County(GameState):
	weather_choices = ["clear skies", "stormy", "sunny", "cloudy", "light rain", "overcast"]

	name = db.Column(db.String(128), nullable=False)
	leader = db.Column(db.String(128))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	kingdom_id = db.Column(db.Integer, db.ForeignKey('kingdom.id'), nullable=False)
	vote = db.Column(db.Integer)
	last_vote_date = db.Column(db.DateTime)

	total_land = db.Column(db.Integer)
	race = db.Column(db.String(32))
	gender = db.Column(db.String(16))
	tax = db.Column(db.Integer)
	gold = db.Column(db.Integer)
	wood = db.Column(db.Integer)
	iron = db.Column(db.Integer)
	rations = db.Column(db.String(32))
	happiness = db.Column(db.Integer)  # Out of 100
	population = db.Column(db.Integer)
	hunger = db.Column(db.Integer)  # Out of 100
	weather = db.Column(db.String(32))
	title = db.Column(db.String(32))
	production = db.Column(db.Integer)
	food_stores = db.Column(db.Integer)
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

		self.population = 500
		self.total_land = 150
		self.hunger = 75
		self.happiness = 75
		self.tax = 5
		self.gold = 1000
		self.wood = 100
		self.iron = 25
		self.rations = "Normal"
		self.production = 0  # How many buildings you can build per day
		self.food_stores = 0
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

	def get_available_land(self):
		"""
		How much land you have which is empty and can be built upon.
		"""
		return sum(building.amount + building.pending for building in self.buildings.values())

	def get_votes_for_self(self):
		"""
		Checks how many counties have voted for you to be king
		"""
		return County.query.filter_by(vote=self.id, kingdom_id=self.kingdom.id).count()

	def can_vote(self):
		if self.last_vote_date and datetime.now() < (self.last_vote_date - timedelta(hours=24)):
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
		return sum(army.amount + army.pending for army in self.armies.values())

	def get_maintenance_workers(self):
		"""
		Returns the population who are maintaining current buildings.
		"""
		return sum(building.labour * building.amount for building in self.buildings.values())

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

	def get_offensive_strength(self, army):
		"""
		Returns the attack power of your army
		"""
		strength = 0
		for unit in self.armies.values():
			strength += army[unit.base] * unit.attack
		strength *= uniform(0.85, 1.15)
		return int(strength)

	def get_defensive_strength(self):
		strength = 0
		for unit in self.armies.values():
			strength += unit.amount * unit.defence
		strength *= uniform(0.9, 1.1)
		return int(strength)

	def get_casualties(self, army={}, ratio=1):
		"""
		Maybe move to a math transform file.
		army: For attacker, the army is passed in as dict. For defender, it's all active troops.
		ratio: The greater you outnumber the enemy, the safer your troops are.
		"""
		casualties = 0
		if army:
			for unit in self.armies.values():
				if army[unit.base] > 0:
					raw_dead = army[unit.base] / uniform(1.4, 1.8) / ratio
					dead = int(raw_dead / unit.health)
					unit.amount -= dead
					casualties += dead
		else:
			for unit in self.armies.values():
				if unit.amount > 0:
					dead = randint(unit.amount // 10, unit.amount // 5)
					unit.amount -= dead
					casualties += dead
		return casualties

	def battle_results(self, army, enemy):
		offence = self.get_offensive_strength(army)
		# offence = get_attack_power(self.id, army)
		defence = enemy.get_defensive_strength()
		offence_casaulties = self.get_casualties(army=army, ratio=(offence / defence))
		defence_casaulties = enemy.get_casualties(army={}, ratio=1)
		if offence > defence:
			land_gained = int(enemy.total_land * 0.1)
			self.total_land += land_gained
			enemy.total_land -= land_gained
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
		db.session.add(notification)
		db.session.commit()
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

	def display_news(self):
		events = [event for event in Notification.query.filter_by(county_id=self.id).all() if event.new is True]
		for event in events:
			event.new = False
		db.session.commit()
		return events

	def get_gold_income(self):
		return int((self.population * (self.tax / 100)) + self.production)

	def get_wood_income(self):
		return self.buildings['mills'].amount * 1

	def get_iron_income(self):
		return self.buildings['mines'].amount * 1

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
		birth_rate = self.buildings['houses'].amount
		return int(birth_rate * modifier)

	def get_immigration_rate(self):
		return randint(20, 30)

	def get_emmigration_rate(self):
		return randint(100, 125) - self.happiness

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
				 and building.production <= self.production]
		if queue and self.production > 0:
			building = choice(queue)
			building.pending -= 1
			building.amount += 1
			self.production -= building.production
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
		if self.weather == 'stormy':
			notification = Notification(self.id, "Storms have ravaged your crops",
										"You lost 20 bushels of wheat.", self.kingdom.world.day)
			db.session.add(notification)
			db.session.commit()

	def update_food(self):
		daily_food = self.buildings['pastures'].amount * 25
		storable_food = self.buildings['fields'].amount * 20
		total_food = daily_food + storable_food + self.food_stores
		food_eaten = self.population * rations_translations_tables[self.rations]
		if total_food >= food_eaten:
			self.food_stores += min(total_food - food_eaten, storable_food)
			self.hunger = min(self.hunger + 1, 100)
		else:
			self.food_stores = 0
			self.hunger -= max(int((food_eaten / total_food) * 5), 0)

	def update_population(self):
		self.deaths = self.get_death_rate()
		self.emigration = self.get_emmigration_rate()
		self.births = self.get_birth_rate()
		self.immigration = self.get_immigration_rate()
		self.population += (self.births + self.immigration) - (self.deaths + self.emigration)

	def get_production(self):
		return max(int(self.get_production_modifier() * self.get_available_workers() / 3), 0)

	@property
	def hunger_terminology(self):
		if self.hunger < 20:
			return "Dying of hunger"
		if self.hunger < 50:
			return "Starving"
		if self.hunger < 75:
			return "Hungry"
		if self.hunger < 90:
			return "Sated"
		return "Well nourished"

	@property
	def happiness_terminology(self):
		if self.happiness < 20:
			return "Rioting"
		if self.happiness < 50:
			return "Furious"
		if self.happiness < 75:
			return "Discontent"
		if self.happiness < 90:
			return "Content"
		return "Pleased"

	def __repr__(self):
		return '<County %r (%r)>' % (self.name, self.id)
