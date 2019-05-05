from extensions import flask_db as db
from .bases import GameEvent


class Session(GameEvent):
    time_logged_out = db.Column(db.DateTime)
    user_id = db.Column(db.Integer)
    county_day = db.Column(db.Integer)
    minutes = db.Column(db.Integer)

    def __init__(self, user_id, county_day):
        self.user_id = user_id
        self.county_day = county_day
        self.seconds = None
        self.valid = True

    def set_minutes(self):
        if self.time_logged_out == self.time_created:
            self.minutes = 0
        else:
            self.minutes = (self.time_logged_out - self.time_created).seconds // 60
