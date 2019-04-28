from datetime import datetime, timedelta

from extensions import flask_db as db
from undyingkingdoms.models import Session, User
from undyingkingdoms.models.bases import GameEvent


class DAU(GameEvent):
    # User data
    user_id = db.Column(db.Integer)
    county_id = db.Column(db.Integer)
    account_age_in_days = db.Column(db.Integer)
    sessions = db.Column(db.Integer)
    minutes_played = db.Column(db.Integer)
    ads_watched = db.Column(db.Integer)
    # Game data
    world_day = db.Column(db.Integer)
    county_day = db.Column(db.Integer)
    score = db.Column(db.Integer)
    land = db.Column(db.Integer)
    population = db.Column(db.Integer)
    happiness = db.Column(db.Integer)
    healthiness = db.Column(db.Integer)
    # Resources
    gold = db.Column(db.Integer)
    wood = db.Column(db.Integer)
    iron = db.Column(db.Integer)
    stone = db.Column(db.Integer)
    research = db.Column(db.Integer)
    mana = db.Column(db.Integer)
    grain = db.Column(db.Integer)
    lifetime_gold = db.Column(db.Integer)
    lifetime_wood = db.Column(db.Integer)
    lifetime_iron = db.Column(db.Integer)
    lifetime_stone = db.Column(db.Integer)
    lifetime_research = db.Column(db.Integer)
    lifetime_mana = db.Column(db.Integer)
    # Choices
    production_choice = db.Column(db.Integer)
    research_choice = db.Column(db.String(128))
    rations = db.Column(db.Float)
    taxes = db.Column(db.Integer)
    technologies = db.Column(db.Integer)
    # Military data
    peasant = db.Column(db.Integer)
    soldier = db.Column(db.Integer)
    archer = db.Column(db.Integer)
    besieger = db.Column(db.Integer)
    summon = db.Column(db.Integer)
    elite = db.Column(db.Integer)
    monster = db.Column(db.Integer)
    maximum_offense = db.Column(db.Integer)
    maximum_defence = db.Column(db.Integer)
    # Building Data
    house = db.Column(db.Integer)
    field = db.Column(db.Integer)
    pasture = db.Column(db.Integer)
    mill = db.Column(db.Integer)
    mine = db.Column(db.Integer)
    fort = db.Column(db.Integer)
    stables = db.Column(db.Integer)
    bank = db.Column(db.Integer)
    tavern = db.Column(db.Integer)
    tower = db.Column(db.Integer)
    lab = db.Column(db.Integer)
    arcane = db.Column(db.Integer)
    quarry = db.Column(db.Integer)
    lair = db.Column(db.Integer)

    def __init__(self, user_id):
        self.user_id = user_id
        self.update_self(user_id)
        self.sessions = self.get_sessions(user_id)
        self.minutes_played = self.get_minutes_played(user_id)
        self.ads_watched = 0

    def update_self(self, user_id):
        user = User.query.get(user_id)
        county = user.county
        
        self.world_day = county.kingdom.world.day
        self.county_day = county.day
        self.account_age_in_days = (datetime.utcnow() - user.time_created).days
        self.county_id = county.id
        self.land = county.land
        self.population = county.population
        self.gold = county.gold
        self.wood = county.wood
        self.iron = county.iron
        self.stone = county.stone
        self.research = county.research
        self.mana = county.mana
        self.grain = county.grain_stores
        self.lifetime_gold = county.lifetime_gold
        self.lifetime_wood = county.lifetime_wood
        self.lifetime_iron = county.lifetime_iron
        self.lifetime_stone = county.lifetime_stone
        self.lifetime_research = county.lifetime_research
        self.lifetime_mana = county.lifetime_mana
        self.happiness = county.happiness
        self.healthiness = county.healthiness

        self.production_choice = county.production_choice
        self.research_choice = county.research_choice
        self.rations = county.rations
        self.taxes = county.tax_rate
        self.technologies = len(county.technologies)
        
        self.peasant = county.armies['peasant'].total
        self.soldier = county.armies['soldier'].total
        self.archer = county.armies['archer'].total
        self.besieger = county.armies['besieger'].total
        self.summon = county.armies['summon'].total
        self.elite = county.armies['elite'].total
        self.monster = county.armies['monster'].total
        self.maximum_offense = county.get_offensive_strength(scoreboard=True)
        self.maximum_defence = county.get_defensive_strength()

        self.house = county.buildings['house'].total
        self.field = county.buildings['field'].total
        self.pasture = county.buildings['pasture'].total
        self.mill = county.buildings['mill'].total
        self.mine = county.buildings['mine'].total
        self.fort = county.buildings['fort'].total
        self.stables = county.buildings['stables'].total
        self.bank = county.buildings['bank'].total
        self.tavern = county.buildings['tavern'].total
        self.tower = county.buildings['tower'].total
        self.lab = county.buildings['lab'].total
        self.arcane = county.buildings['arcane'].total
        self.quarry = county.buildings['quarry'].total
        self.lair = county.buildings['lair'].total

    @staticmethod
    def get_sessions(user_id):
        time_cutoff = datetime.utcnow() - timedelta(hours=1)
        return Session.query.filter_by(user_id=user_id).filter(Session.time_logged_out > time_cutoff).count()

    @staticmethod
    def get_minutes_played(user_id):
        time_cutoff = datetime.utcnow() - timedelta(hours=1)
        sessions = Session.query.filter_by(user_id=user_id).filter(Session.time_logged_out > time_cutoff).all()
        return sum(session.minutes for session in sessions if session.minutes is not None)
