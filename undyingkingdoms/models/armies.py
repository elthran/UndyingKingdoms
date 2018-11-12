from undyingkingdoms import db
from undyingkingdoms.models.bases import GameState


class Army(GameState):
    county_id = db.Column(db.Integer, db.ForeignKey('county.id', ondelete="CASCADE"), nullable=False)
    base = db.Column(db.String(64))
    name = db.Column(db.String(64))
    amount = db.Column(db.Integer)
    pending = db.Column(db.Integer)
    training = db.Column(db.Integer)
    gold = db.Column(db.Integer)
    iron = db.Column(db.Integer)
    wood = db.Column(db.Integer)
    attack = db.Column(db.Integer)
    defence = db.Column(db.Integer)
    health = db.Column(db.Integer)
    description = db.Column(db.String(128))

    def __init__(self, base, name, amount, training, gold, iron, wood, attack, defence, health, description):
        self.base = base
        self.name = name
        self.amount = amount
        self.pending = 0
        self.training = training  # Number than can train per game-day
        self.gold = gold
        self.iron = iron
        self.wood = wood
        self.attack = attack
        self.defence = defence
        self.health = health
        self.description = description
