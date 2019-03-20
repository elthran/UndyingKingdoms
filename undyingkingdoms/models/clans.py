from undyingkingdoms.models.bases import GameEvent, db


class Clan(GameEvent):

    kingdom_id = db.Column(db.Integer, db.ForeignKey('kingdom.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner = db.Column(db.Boolean)

    def __init__(self, kingdom_id, user_id, owner):

        self.kingdom_id = kingdom_id
        self.user_id = user_id
        self.owner = owner

