from datetime import datetime

from sqlalchemy import desc

from undyingkingdoms import db
from undyingkingdoms.models.bases import GameEvent


class Session(GameEvent):
    user_id = db.Column(db.Integer)
    activity = db.Column(db.String(16))
    minutes = db.Column(db.Integer)
    ip_address = db.Column(db.String(32))

    def __init__(self, user_id, activity):
        self.user_id = user_id
        self.activity = activity
        self.minutes = self.get_minutes()
        self.ip_address = "Unknown"

    def get_minutes(self):
        if self.activity == "logout":
            last_login = Session.query.filter_by(user_id=self.user_id, activity="login").order_by(desc('date_created')).first()
            if last_login:
                time_difference = (datetime.now() - last_login.date_created)
                return time_difference.seconds // 60
        return -1
