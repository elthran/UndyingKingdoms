from undyingkingdoms import db
from undyingkingdoms.models.bases import GameState


class Building(GameState):
    county_id = db.Column(db.Integer, db.ForeignKey('county.id', ondelete="CASCADE"), nullable=False)
    base = db.Column(db.String(64))
    name = db.Column(db.String(64))
    amount = db.Column(db.Integer)
    pending = db.Column(db.Integer)
    production = db.Column(db.Integer)
    labour = db.Column(db.Integer)
    gold = db.Column(db.Integer)
    wood = db.Column(db.Integer)
    maintenance = db.Column(db.Integer)

    def __init__(self, base, name, amount, production, labour, gold, wood, description):
        self.base = base
        self.name = name
        self.amount = amount
        self.pending = 0
        self.production = production  # Amount of work to build it
        self.labour = labour  # Amount of workers to use it
        self.gold = gold  # Gold cost to build it
        self.wood = wood  # Wood cost to build it
        self.description = description
