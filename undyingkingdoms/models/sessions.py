from datetime import datetime

from extensions import flask_db as db
from undyingkingdoms.models.bases import GameEvent


class Session(GameEvent):
    time_logged_out = db.Column(db.DateTime)
    user_id = db.Column(db.Integer)
    minutes = db.Column(db.Integer)

    def __init__(self, user_id):
        self.user_id = user_id
        self.seconds = None
        self.valid = True

    def set_minutes(self):
        self.minutes = (self.time_logged_out - self.time_created).seconds // 60

