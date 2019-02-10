from undyingkingdoms.models.bases import GameEvent, db


class Trade(GameEvent):

    county_id = db.Column(db.Integer, db.ForeignKey('county.id'), nullable=False)
    target_id = db.Column(db.Integer)
    world_day = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    accepted = db.Column(db.Boolean)

    gold = db.Column(db.Integer)
    wood = db.Column(db.Integer)
    iron = db.Column(db.Integer)

    def __init__(self, county_id, target_id, world_day, duration, gold=0, wood=0, iron=0):

        self.county_id = county_id
        self.target_id = target_id
        self.world_day = world_day
        self.duration = duration
        self.accepted = "pending"

        self.gold = gold
        self.wood = wood
        self.iron = iron

