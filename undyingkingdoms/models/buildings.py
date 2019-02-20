from extensions import flask_db as db
from undyingkingdoms.models.bases import GameState


class Building(GameState):
    county_id = db.Column(db.Integer, db.ForeignKey('county.id', ondelete="CASCADE"), nullable=False)
    name = db.Column(db.String(64))
    class_name = db.Column(db.String(64))
    class_name_plural = db.Column(db.String(64))
    total = db.Column(db.Integer)
    pending = db.Column(db.Integer)
    workers_employed = db.Column(db.Integer)
    gold_cost = db.Column(db.Integer)
    wood_cost = db.Column(db.Integer)
    stone_cost = db.Column(db.Integer)
    output = db.Column(db.Integer)  # How much x it produces
    description = db.Column(db.String(128))

    def __init__(self, name, class_name, class_name_plural, total, workers_employed, gold_cost, wood_cost, stone_cost, output, description):
        self.name = name
        self.class_name = class_name
        self.class_name_plural = class_name_plural
        self.total = total
        self.pending = 0
        self.workers_employed = workers_employed  # Amount of workers to use it
        self.gold_cost = gold_cost
        self.wood_cost = wood_cost
        self.stone_cost = stone_cost
        self.output = output
        self.description = description.format(self.class_name, self.output)
