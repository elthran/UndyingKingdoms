from undyingkingdoms import db
from undyingkingdoms.models.bases import GameEvent


class Achievement(GameEvent):

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(64))
    description = db.Column(db.String(64))
    points = db.Column(db.Integer)

    def __init__(self, user_id, name, description, points=5):
        self.user_id = user_id
        self.name = name
        self.description = description
        self.points = points

    def validate(self):
        if not isinstance(self.name, str):
            return False
        if not isinstance(self.user_id, int):
            return False
        return True
