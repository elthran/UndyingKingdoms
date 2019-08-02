import hashlib
from copy import deepcopy

from sqlalchemy import desc
from sqlalchemy.orm.collections import attribute_mapped_collection

from .sessions import Session
from .achievements import Achievement
from .bases import GameState, db
from werkzeug.security import generate_password_hash, check_password_hash
from app.metadata.metadata_achievements import all_achievements


class User(GameState):
    # Basic data
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password_hash = db.Column(db.String(192), nullable=False)
    gems = db.Column(db.Integer)

    # Analytics
    ages_completed = db.Column(db.Integer)
    day1_retention = db.Column(db.Integer)
    day3_retention = db.Column(db.Integer)
    day7_retention = db.Column(db.Integer)
    lifetime_revenue = db.Column(db.Integer)
    country = db.Column(db.String(32))
    _in_active_session = db.Column(db.Boolean)

    tutorials = db.relationship('Tutorial', backref='user')

    # Achievements
    achievements = db.relationship("Achievement",
                                   collection_class=attribute_mapped_collection('name'),
                                   cascade="all, delete, delete-orphan", passive_deletes=True)
    achievement_points = db.Column(db.Integer)

    # Flask
    is_authenticated = db.Column(db.Boolean)  # User has logged in through flask. (Flask)
    is_active = db.Column(db.Boolean)  # Account has been activated via email and not been locked. (Flask)
    is_anonymous = db.Column(db.Boolean)  # Current_user is set to is_anonymous when not yet logged in. (Flask)
    is_verified = db.Column(db.Boolean)
    is_admin = db.Column(db.Boolean)  # Current user is a game creator with unlimited power
    is_bot = db.Column(db.Boolean)  # Current user is a game creator with unlimited power

    def __init__(self, username, email, password, is_bot=False):
        # Basic data
        self.username = username
        self.email = email
        self.set_password_hash(password)
        self.gems = 0

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
        self.is_verified = False  # Custom: for email validation
        
        # Administrative
        self.is_admin = False
        self.is_bot = is_bot

    @property
    def in_active_session(self):
        return self._in_active_session

    @in_active_session.setter
    def in_active_session(self, value):
        self._in_active_session = value
        if value:  # Logging in
            try:  # if the user doesn't have a county yet.
                day = self.county.kingdom.world.day
            except AttributeError:
                day = None
            last_session = Session.query.filter_by(user_id=self.id).order_by(desc('time_created')).first()
            if not last_session:  # Never logged in before
                session = Session(self.id, day)
                session.save()
            else:  # Has logged in before
                if last_session.time_logged_out:  # Last session successfully logged out
                    session = Session(self.id, day)  # Simply start a new log in
                    session.save()
                else:
                    last_session.time_logged_out = self.time_modified
                    session = Session(self.id, day)
                    session.save()
        else:  # Logging out
            session = Session.query.filter_by(user_id=self.id).order_by(desc('time_created')).first()
            if session:
                session.time_logged_out = self.time_modified
                session.set_minutes()

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute. Only password_hash is stored.')

    def set_password_hash(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_verification_hash(self):
        email_hash = hashlib.md5(self.password_hash.encode())
        # if hash is too long it isn't selectable
        return email_hash.hexdigest()[:-2]

    def verify_verification_hash(self, hash):
        if hash == self.generate_verification_hash():
            return True
        return False

    def get_id(self):
        return self.id

    def has_county(self):
        return True if self.county is not None else False

    def check_incremental_achievement(self, name, amount):
        achievement = Achievement.query.filter_by(category="reach_x_amount_in_one_age",
                                                  sub_category=name,
                                                  user_id=self.id).first()
        if achievement.current_tier < achievement.maximum_tier:
            requirement_to_advance = getattr(achievement, "tier" + str(achievement.current_tier + 1))
            if amount >= requirement_to_advance:
                achievement.current_tier += 1
                self.achievement_points += achievement.points_rewarded

    def get_last_logout(self):
        session = Session.query.filter_by(user_id=self.id).order_by(desc('time_created')).first()
        if session is None:
            return False
        return session.time_logged_out

    def get_previous_session(self):
        session = Session.query.filter_by(user_id=self.id).order_by(desc('time_logged_out')).first()
        if session is None:
            return False
        return session.time_created

    def __repr__(self):
        return '<User %r (%r)>' % (self.username, self.id)
