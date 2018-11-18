from undyingkingdoms import db
from undyingkingdoms.models.bases import GameEvent


class Achievement(GameEvent):

    user_id = db.Column(db.Integer)
    name = db.Column(db.String(64))
    description = db.Column(db.String(64))

    def __init__(self, user_id, name, description):
        self.user_id = user_id
        self.name = name
        self.description = description

    def validate(self):
        if not isinstance(self.name, str):
            return False
        if not isinstance(self.user_id, int):
            return False
        return True
