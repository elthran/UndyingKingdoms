from undyingkingdoms import db
from undyingkingdoms.models.bases import GameEvent


class AuthenticationEvent(GameEvent):

    session_length = db.Column(db.Integer)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session_length = 0

    @property
    def validate(self):
        if not isinstance(self.user_id, int):
            return False
        if not isinstance(self.activity, str) or self.activity not in ['login', 'logout']:
            return False
        return True

