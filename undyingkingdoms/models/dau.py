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
    world_age_in_days = db.Column(db.Integer)
    county_days_in_age = db.Column(db.Integer)
    current_score = db.Column(db.Integer)
    land = db.Column(db.Integer)
    population = db.Column(db.Integer)
    gold = db.Column(db.Integer)
    happiness = db.Column(db.Integer)
    hunger = db.Column(db.Integer)
    # Military data
    peasants = db.Column(db.Integer)
    soldiers = db.Column(db.Integer)
    archers = db.Column(db.Integer)
    elites = db.Column(db.Integer)
    # Building Data
    houses = db.Column(db.Integer)
    fields = db.Column(db.Integer)
    pastures = db.Column(db.Integer)
    mills = db.Column(db.Integer)
    mines = db.Column(db.Integer)
    forts = db.Column(db.Integer)
    stables = db.Column(db.Integer)
    guilds = db.Column(db.Integer)

    def __init__(self, user_id, county_days_in_age, world_age_in_days):
        self.user_id = user_id
        self.county_days_in_age = county_days_in_age
        self.world_age_in_days = world_age_in_days
        self.sessions = self.get_sessions(user_id)
        self.minutes_played = self.get_minutes_played(user_id)
        self.ads_watched = 0
        self.update_self(user_id)

    def update_self(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        county = user.county
        
        self.account_age_in_days = (datetime.utcnow() - user.time_created).days
        self.county_id = county.id
        self.current_score = user.get_current_leaderboard_score()
        self.land = county.land
        self.population = county.population
        self.gold = county.gold
        self.happiness = county.happiness
        self.hunger = county.hunger
        
        self.peasants = county.armies['peasant'].total
        self.soldiers = county.armies['soldier'].total
        self.archers = county.armies['archer'].total
        self.elites = county.armies['elite'].total

        self.houses = county.buildings['houses'].total
        self.fields = county.buildings['fields'].total
        self.pastures = county.buildings['pastures'].total
        self.mills = county.buildings['mills'].total
        self.mines = county.buildings['mines'].total
        self.forts = county.buildings['forts'].total
        self.stables = county.buildings['stables'].total
        self.guilds = county.buildings['guilds'].total

    @staticmethod
    def get_sessions(user_id):
        time_cutoff = datetime.utcnow() - timedelta(hours=4)
        return Session.query.filter_by(user_id=user_id).filter(Session.time_logged_out > time_cutoff).count()

    @staticmethod
    def get_minutes_played(user_id):
        time_cutoff = datetime.utcnow() - timedelta(hours=4)
        sessions = Session.query.filter_by(user_id=user_id).filter(Session.time_logged_out > time_cutoff).all()
        return sum(session.minutes for session in sessions if session.minutes is not None)
