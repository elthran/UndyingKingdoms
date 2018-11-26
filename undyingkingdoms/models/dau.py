from datetime import datetime, timedelta

from undyingkingdoms import db
from undyingkingdoms.models import Session, User
from undyingkingdoms.models.bases import GameEvent


class DailyActiveUser(GameEvent):
    # User data
    user_id = db.Column(db.Integer)
    account_age_in_days = db.Column(db.Integer)
    todays_sessions = db.Column(db.Integer)
    todays_minutes_played = db.Column(db.Integer)
    todays_ads_watched = db.Column(db.Integer)
    # Game data
    days_in_age = db.Column(db.Integer)
    land = db.Column(db.Integer)
    gold = db.Column(db.Integer)
    happiness = db.Column(db.Integer)
    hunger = db.Column(db.Integer)

    def __init__(self, user_id, day):
        self.user_id = user_id
        self.days_in_age = day
        self.todays_sessions = self.get_sessions(user_id)
        self.todays_minutes_played = self.get_minutes_played(user_id)
        self.update_self(user_id)

    def update_self(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        county = user.county
        self.account_age_in_days = (datetime.now() - user.date_created).days
        self.land = county.total_land
        self.gold = county.gold
        self.happiness = county.happiness
        self.hunger = county.hunger

    def get_sessions(self, user_id):
        # This should filter by timestamp and only return sessions that day
        # Timestamp in filter should match day below
        #yesterday = datetime.now() - timedelta(days=1)
        return Session.query.filter_by(user_id=user_id, activity="login").count()

    def get_minutes_played(self, user_id):
        # This should filter by timestamp and only return sessions that day
        # Timestamp in filter should match day below
        # yesterday = datetime.now() - timedelta(days=1)
        sessions = Session.query.filter_by(user_id=user_id, activity="logout").all()
        return sum(session.minutes for session in sessions)

    def validate(self):
        if not isinstance(self.user_id, int):
            return False
        if not isinstance(self.account_age, int):
            return False
        if not isinstance(self.sessions, int) or self.sessions < 1:
            return False
        if not isinstance(self.minutes_played, int):
            return False
        if not isinstance(self.land, int):
            return False
        if not isinstance(self.gold, int):
            return False
        if not isinstance(self.happiness, int):
            return False
        return True




