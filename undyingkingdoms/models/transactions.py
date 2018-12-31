from extensions import flask_db as db
from undyingkingdoms.models.bases import GameEvent
from undyingkingdoms.static.metadata import all_buildings, all_armies

transactions = ["buy", "sell"]


class Transaction(GameEvent):
    user_id = db.Column(db.Integer)
    days_in_age = db.Column(db.Integer)
    activity = db.Column(db.String(16))
    starting_gold = db.Column(db.Integer)
    starting_wood = db.Column(db.Integer)
    starting_iron = db.Column(db.Integer)

    gold_spent = db.Column(db.Integer)
    wood_spent = db.Column(db.Integer)
    iron_spent = db.Column(db.Integer)

    houses = db.Column(db.Integer)
    fields = db.Column(db.Integer)
    mills = db.Column(db.Integer)
    mines = db.Column(db.Integer)

    peasant = db.Column(db.Integer)
    archer = db.Column(db.Integer)
    soldier = db.Column(db.Integer)
    elite = db.Column(db.Integer)

    def __init__(self, user_id, days_in_age, activity, starting_gold, starting_wood, starting_iron):
        self.user_id = user_id
        self.days_in_age = days_in_age
        self.activity = activity if activity in transactions else "unknown"
        self.starting_gold = starting_gold
        self.starting_wood = starting_wood
        self.starting_iron = starting_iron

        self.houses = 0
        self.fields = 0
        self.mills = 0
        self.mines = 0

        self.peasant = 0
        self.archer = 0
        self.soldier = 0
        self.elite = 0

        self.gold_spent = 0
        self.wood_spent = 0
        self.iron_spent = 0
        self.houses_built = 0

    def add_purchase(self, item_name, item_amount, gold_per_item, wood_per_item, iron_per_item):
        if (item_name not in all_buildings) and (item_name not in all_armies):
            self.activity = "unknown item name"
        else:
            setattr(self, item_name, item_amount)
            self.gold_spent += item_amount * gold_per_item
            self.wood_spent += item_amount * wood_per_item
            self.iron_spent += item_amount * iron_per_item
