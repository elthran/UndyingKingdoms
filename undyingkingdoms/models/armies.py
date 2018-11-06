from undyingkingdoms import db
from undyingkingdoms.models.bases import GameState


class Army(GameState):
    county_id = db.Column(db.Integer,
                          db.ForeignKey('county.id', ondelete="CASCADE"), nullable=False, )
    name = db.Column(db.String(64))
    amount = db.Column(db.Integer)
    pending = db.Column(db.Integer)
    attack = db.Column(db.Integer)
    defence = db.Column(db.Integer)
    health = db.Column(db.Integer)

    def __init__(self, name, amount, attack, defence, health):
        self.name = name
        self.amount = amount
        self.pending = 0
        self.attack = attack
        self.defence = defence
        self.health = health
