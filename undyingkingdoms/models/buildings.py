from undyingkingdoms import db
from undyingkingdoms.models.bases import GameState


class Building(GameState):
    county_id = db.Column(db.Integer, db.ForeignKey('county.id', ondelete="CASCADE"), nullable=False)
    base_name = db.Column(db.String(64))
    class_name = db.Column(db.String(64))
    total = db.Column(db.Integer)
    pending = db.Column(db.Integer)
    production_cost = db.Column(db.Integer)
    labour_maintenance = db.Column(db.Integer)
    gold = db.Column(db.Integer)
    wood = db.Column(db.Integer)
    description = db.Column(db.String(128))

    def __init__(self, base_name, class_name, total, production_cost, labour_maintenance, gold, wood, description):
        self.base_name = base_name
        self.class_name = class_name
        self.total = total
        self.pending = 0
        self.production_cost = production_cost  # Amount of work to build it
        self.labour_maintenance = labour_maintenance  # Amount of workers to use it
        self.gold = gold  # Gold cost to build it
        self.wood = wood  # Wood cost to build it
        self.description = description
