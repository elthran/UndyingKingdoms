from undyingkingdoms import db
from undyingkingdoms.models.bases import GameEvent

transactions = ["buy", "sell"]


class Transaction(GameEvent):
    user_id = db.Column(db.Integer)
    activity = db.Column(db.String(16))
    gold_amount = db.Column(db.Integer)

    def __init__(self, user_id, activity, gold):
        self.user_id = user_id
        self.activity = activity if activity in transactions else "unknown"
        self.gold_amount = gold
