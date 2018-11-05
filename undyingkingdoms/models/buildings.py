from undyingkingdoms import db
from undyingkingdoms.models.bases import GameState


class Building(GameState):
    county_id = db.Column(db.Integer,
                          db.ForeignKey('county.id', ondelete="CASCADE"), nullable=False, )
    name = db.Column(db.String(64))
    amount = db.Column(db.Integer)
    pending = db.Column(db.Integer)
    cost = db.Column(db.Integer)
    maintenance = db.Column(db.Integer)

    def __init__(self, name, amount, cost, maintenance, description):
        self.name = name
        self.amount = amount
        self.pending = 0
        self.cost = cost
        self.maintenance = maintenance
        self.description = description
