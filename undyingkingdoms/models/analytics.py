from datetime import datetime

from undyingkingdoms import db
from undyingkingdoms.models.bases import GameEvent


class AuthenticationEvent(GameEvent):
    activity = db.Column(db.String(32))
    session_id = db.Column(db.Integer)
    session_length = db.Column(db.Integer)

    def __init__(self, user_id, activity="unknown", session_id=-1):
        self.user_id = user_id
        self.activity = activity
        self.session_id = session_id
        self.session_length = self.get_session_length()

    def get_session_length(self):
        if self.activity == 'logout':
            login_event = AuthenticationEvent.query.filter_by(user_id=self.user_id).filter_by(
                session_id=self.session_id).first()
            try:
                delta = datetime.now() - login_event.date_created
                delta_minutes = delta.seconds // 60
            except:
                delta_minutes = 4
            return delta_minutes
        return None
