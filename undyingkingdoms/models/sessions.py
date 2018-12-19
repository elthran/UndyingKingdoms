from datetime import datetime

from sqlalchemy import desc

from undyingkingdoms import db
from undyingkingdoms.models.bases import GameEvent


class Session(GameEvent):
    time_logged_out = db.Column(db.DateTime)
    user_id = db.Column(db.Integer)
    minutes = db.Column(db.Integer)
    valid = db.Column(db.Boolean)

    def __init__(self, user_id, activity):
        self.user_id = user_id
        self.minutes = self.get_minutes()
        self.valid = True
        self.validate(activity)

    def set_minutes(self):
        last_login = Session.query.filter_by(user_id=self.user_id).order_by(desc('time_created')).first()
        if last_login.time_logged_out:  # User has no record of logging in
            self.valid = False
        else:
            time_difference = (datetime.now() - last_login.time_created)
            self.minutes = time_difference.seconds // 60

