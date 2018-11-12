from undyingkingdoms import db
from undyingkingdoms.models.bases import GameEvent


class Achievement(GameEvent):

    name = db.Column(db.String(64))
    user_id = db.Column(db.Integer)

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

    def validate(self):
        if not isinstance(self.name, str):
            return False
        if not isinstance(self.user_id, int):
            return False
        return True
