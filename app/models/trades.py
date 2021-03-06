from .bases import GameEvent, db


class Trade(GameEvent):

    county_id = db.Column(db.Integer, db.ForeignKey('county.id'), nullable=False)
    county = db.relationship(
        "County",
        backref="trades_offered",
        foreign_keys="[Trade.county_id]"
    )
    target_id = db.Column(db.Integer, db.ForeignKey('county.id'), nullable=False)
    target = db.relationship(
        "County",
        backref="trades_received",
        foreign_keys="[Trade.target_id]"
    )

    world_day = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    status = db.Column(db.String(16))

    gold_to_give = db.Column(db.Integer)
    wood_to_give = db.Column(db.Integer)
    iron_to_give = db.Column(db.Integer)
    stone_to_give = db.Column(db.Integer)
    grain_to_give = db.Column(db.Integer)

    gold_to_receive = db.Column(db.Integer)
    wood_to_receive = db.Column(db.Integer)
    iron_to_receive = db.Column(db.Integer)
    stone_to_receive = db.Column(db.Integer)
    grain_to_receive = db.Column(db.Integer)

    def __init__(self, county, target, world_day, duration, gold_to_give=0, wood_to_give=0, iron_to_give=0, stone_to_give=0, grain_to_give=0,
                 gold_to_receive=0, wood_to_receive=0, iron_to_receive=0, stone_to_receive=0, grain_to_receive=0):

        self.county = county
        self.target = target
        self.world_day = world_day
        self.duration = duration
        self.status = "Pending"

        self.gold_to_give = gold_to_give
        self.wood_to_give = wood_to_give
        self.iron_to_give = iron_to_give
        self.stone_to_give = stone_to_give
        self.grain_to_give = grain_to_give

        self.gold_to_receive = gold_to_receive
        self.wood_to_receive = wood_to_receive
        self.iron_to_receive = iron_to_receive
        self.stone_to_receive = stone_to_receive
        self.grain_to_receive = grain_to_receive
