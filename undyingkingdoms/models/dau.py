from datetime import datetime, timedelta

from sqlalchemy import cast, Date

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
    gold = db.Column(db.Integer)
    wood = db.Column(db.Integer)
    iron = db.Column(db.Integer)
    stone = db.Column(db.Integer)
    lifetime_gold = db.Column(db.Integer)
    lifetime_wood = db.Column(db.Integer)
    lifetime_iron = db.Column(db.Integer)
    lifetime_stone = db.Column(db.Integer)
    happiness = db.Column(db.Integer)
    nourishment = db.Column(db.Integer)
    health = db.Column(db.Integer)
    # Military data
    peasant = db.Column(db.Integer)
    soldier = db.Column(db.Integer)
    archer = db.Column(db.Integer)
    elite = db.Column(db.Integer)
    monster = db.Column(db.Integer)
    # Building Data
    house = db.Column(db.Integer)
    field = db.Column(db.Integer)
    pasture = db.Column(db.Integer)
    mill = db.Column(db.Integer)
    mine = db.Column(db.Integer)
    fort = db.Column(db.Integer)
    stables = db.Column(db.Integer)
    guild = db.Column(db.Integer)
    bank = db.Column(db.Integer)
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
        self.score = user.get_current_leaderboard_score()
        self.land = county.land
        self.population = county.population
        self.gold = county.gold
        self.wood = county.wood
        self.iron = county.iron
        self.stone = county.stone
        self.lifetime_gold = county.lifetime_gold
        self.lifetime_wood = county.lifetime_wood
        self.lifetime_iron = county.lifetime_iron
        self.lifetime_stone = county.lifetime_stone
        self.happiness = county.happiness
        self.nourishment = county.nourishment
        self.health = county.health
        
        self.peasant = county.armies['peasant'].total
        self.soldier = county.armies['soldier'].total
        self.archer = county.armies['archer'].total
        self.elite = county.armies['elite'].total
        self.monster = county.armies['monster'].total

        self.house = county.buildings['house'].total
        self.field = county.buildings['field'].total
        self.pasture = county.buildings['pasture'].total
        self.mill = county.buildings['mill'].total
        self.mine = county.buildings['mine'].total
        self.fort = county.buildings['fort'].total
        self.stables = county.buildings['stables'].total
        self.guild = county.buildings['guild'].total
        self.bank = county.buildings['bank'].total
        self.quarry = county.buildings['quarry'].total
        self.lair = county.buildings['lair'].total

    @staticmethod
    def get_sessions(user_id):
        time_cutoff = datetime.utcnow() - timedelta(hours=4)
        return Session.query.filter_by(user_id=user_id).filter(Session.time_logged_out > time_cutoff).count()

    @staticmethod
    def get_minutes_played(user_id):
        time_cutoff = datetime.utcnow() - timedelta(hours=4)
        sessions = Session.query.filter_by(user_id=user_id).filter(Session.time_logged_out > time_cutoff).all()
        return sum(session.minutes for session in sessions if session.minutes is not None)
