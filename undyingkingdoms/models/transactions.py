from extensions import flask_db as db
from undyingkingdoms.models.bases import GameEvent
from undyingkingdoms.static.metadata.metadata import all_buildings, all_armies

transactions = ["buy", "sell"]


class Transaction(GameEvent):
    county_id = db.Column(db.Integer)
    county_day = db.Column(db.Integer)
    world_day = db.Column(db.Integer)
    activity = db.Column(db.String(16))

    gold_spent = db.Column(db.Integer)
    wood_spent = db.Column(db.Integer)
    iron_spent = db.Column(db.Integer)
    stone_spent = db.Column(db.Integer)

    house = db.Column(db.Integer)
    field = db.Column(db.Integer)
    pasture = db.Column(db.Integer)
    mill = db.Column(db.Integer)
    mine = db.Column(db.Integer)
    fort = db.Column(db.Integer)
    stables = db.Column(db.Integer)
    tavern = db.Column(db.Integer)
    bank = db.Column(db.Integer)
    quarry = db.Column(db.Integer)
    lair = db.Column(db.Integer)

    peasant = db.Column(db.Integer)
    archer = db.Column(db.Integer)
    soldier = db.Column(db.Integer)
    elite = db.Column(db.Integer)
    monster = db.Column(db.Integer)

    def __init__(self, county_id, county_day, world_day, activity):
        self.county_id = county_id
        self.county_day = county_day
        self.world_day = world_day
        self.activity = activity if activity in transactions else "unknown"

        self.house = 0
        self.field = 0
        self.pasture = 0
        self.mill = 0
        self.mine = 0
        self.fort = 0
        self.stables = 0
        self.tavern = 0
        self.bank = 0
        self.quarry = 0
        self.lair = 0

        self.peasant = 0
        self.archer = 0
        self.soldier = 0
        self.elite = 0
        self.monster = 0

        self.gold_spent = 0
        self.wood_spent = 0
        self.iron_spent = 0
        self.stone_spent = 0

    def add_purchase(self, item_name='Unknown', item_amount=0, gold_per_item=0, wood_per_item=0, iron_per_item=0, stone_per_item=0):
        if (item_name not in all_buildings) and (item_name not in all_armies):
            self.activity = "unknown item name"
        else:
            setattr(self, item_name, item_amount)
            self.gold_spent += item_amount * gold_per_item
            self.wood_spent += item_amount * wood_per_item
            self.iron_spent += item_amount * iron_per_item
            self.stone_spent += item_amount * stone_per_item
