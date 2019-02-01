from copy import deepcopy
from datetime import datetime

from sqlalchemy import desc
from sqlalchemy.orm.collections import attribute_mapped_collection

from undyingkingdoms.models.sessions import Session
from undyingkingdoms.models.achievements import Achievement
from undyingkingdoms.models.bases import GameState, db
from werkzeug.security import generate_password_hash, check_password_hash
from undyingkingdoms.models.counties import County
from undyingkingdoms.static.metadata import all_achievements


class User(GameState):
    # Basic data
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password_hash = db.Column(db.String(192), nullable=False)
    phone_number = db.Column(db.Integer)
    county = db.relationship('County', backref='user', uselist=False)

    # Analytics
    ages_completed = db.Column(db.Integer)
    day1_retention = db.Column(db.Integer)
    day3_retention = db.Column(db.Integer)
    day7_retention = db.Column(db.Integer)
    lifetime_revenue = db.Column(db.Integer)
    country = db.Column(db.String(32))
    _in_active_session = db.Column(db.Boolean)

    # Achievements
    achievements = db.relationship("Achievement",
                                   collection_class=attribute_mapped_collection('name'),
                                   cascade="all, delete, delete-orphan", passive_deletes=True)
    achievement_points = db.Column(db.Integer)
    alpha_wins = db.Column(db.Integer)

    # Flask
    is_authenticated = db.Column(db.Boolean)  # User has logged in
    is_active = db.Column(db.Boolean)  # Account has been activated via email and not been locked
    is_anonymous = db.Column(db.Boolean)  # current_user is set to is_anonymous when not yet logged in.
    is_admin = db.Column(db.Boolean)  # Current user is a game creator with unlimited power
    is_bot = db.Column(db.Boolean)  # Current user is a game creator with unlimited power

    def __init__(self, username, email, password):
        # Basic data
        self.username = username
        self.email = email
        self.set_password_hash(password)

        # Analytics
        self.ages_completed = 0
        self.day1_retention = None
        self.day3_retention = None
        self.day7_retention = None
        self.lifetime_revenue = 0
        self.country = ""
        self._in_active_session = False

        # Achievements
        self.achievements = deepcopy(all_achievements)
        self.achievement_points = 0

        # Flask login
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False
        
        # Administrative
        self.is_admin = False
        self.is_bot = False

        self.alpha_wins = 0

    @property
    def in_active_session(self):
        return self._in_active_session

    @in_active_session.setter
    def in_active_session(self, value):
        self._in_active_session = value
        if value:  # Logging in
            session = Session(self.id)
            session.save()
        else:  # Logging out
            session = Session.query.filter_by(user_id=self.id).order_by(desc('time_created')).first()
            if session:
                session.time_logged_out = datetime.now()
                session.set_minutes()

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute. Only password_hash is stored.')

    def set_password_hash(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.id

    def has_county(self):
        return True if County.query.filter_by(user_id=self.id) else False

    def check_incremental_achievement(self, name, amount):
        achievement = Achievement.query.filter_by(category="reach_x_amount_in_one_age",
                                                  sub_category=name,
                                                  user_id=self.id).first()
        if achievement.current_tier < achievement.maximum_tier:
            requirement_to_advance = getattr(achievement, "tier" + str(achievement.current_tier + 1))
            if amount >= requirement_to_advance:
                achievement.current_tier += 1
                self.achievement_points += achievement.points_rewarded

    def get_last_login(self):
        session = Session.query.filter_by(user_id=self.id).order_by(desc('time_created')).first()
        if session is None:
            return self.time_created
        return session.time_created

    def get_current_leaderboard_score(self):
        # TEMPORARY FOR ALPHA. Just a quick way to add some fun
        score = self.county.land * 10
        score += self.county.population // 2
        score += max(self.county.get_offensive_strength(scoreboard=True), self.county.get_defensive_strength(scoreboard=True))
        return score

    def __repr__(self):
        return '<User %r (%r)>' % (self.username, self.id)
