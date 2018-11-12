from undyingkingdoms import db
from undyingkingdoms.models import AuthenticationEvent, County
from undyingkingdoms.models.bases import GameEvent


class DailyActiveUserEvent(GameEvent):

    days_in_age = db.Column(db.Integer)
    account_age = db.Column(db.Integer)
    sessions = db.Column(db.Integer)
    minutes_played = db.Column(db.Integer)
    land = db.Column(db.Integer)
    gold = db.Column(db.Integer)
    happiness = db.Column(db.Integer)

    def __init__(self, user_id):
        self.user_id = user_id
        self.days_in_age = -1
        self.account_age = -1
        self.sessions = -1
        self.minutes_played = -1
        self.land = -1
        self.gold = -1
        self.happiness = -1

    def get_daily_stats(self):
        county = County.query.filter_by(user_id=self.user_id).first()
        self.get_sessions()
        self.get_minutes_played()
        self.get_land(county)
        self.get_gold(county)
        self.get_happiness(county)

    def get_sessions(self):
        self.sessions = len(AuthenticationEvent.query.filter_by(user_id=self.user_id).filter_by(activity='login').all())

    @staticmethod
    def get_minutes_played():
        return -1

    def get_land(self, county):
        self.land = county.total_land

    def get_gold(self, county):
        self.gold = county.gold

    def get_happiness(self, county):
        self.happiness = county.happiness

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




