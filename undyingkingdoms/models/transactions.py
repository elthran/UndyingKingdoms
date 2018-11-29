from undyingkingdoms import db
from undyingkingdoms.models.bases import GameEvent
from undyingkingdoms.static.metadata import all_buildings

transactions = ["buy", "sell"]


class Transaction(GameEvent):
    user_id = db.Column(db.Integer)
    days_in_age = db.Column(db.Integer)
    activity = db.Column(db.String(16))
    county_gold = db.Column(db.Integer)

    gold_spent = db.Column(db.Integer)
    houses = db.Column(db.Integer)
    fields = db.Column(db.Integer)
    mills = db.Column(db.Integer)
    mines = db.Column(db.Integer)

    def __init__(self, user_id, days_in_age, activity, county_gold):
        self.user_id = user_id
        self.days_in_age = days_in_age
        self.activity = activity if activity in transactions else "unknown"
        self.county_gold = county_gold

        self.houses = 0
        self.fields = 0
        self.mills = 0
        self.mines = 0

        self.gold_spent = 0
        self.houses_built = 0

    def add_purchase(self, item_name, item_amount, gold_per_item):
        if item_name not in all_buildings:
            self.activity = "unknown item name"
        else:
            setattr(self, item_name, item_amount)
            self.gold += item_amount * gold_per_item
