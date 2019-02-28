from undyingkingdoms.models.bases import GameEvent, db


class Diplomacy(GameEvent):

    county_id = db.Column(db.Integer, db.ForeignKey('county.id'), nullable=False)
    target_id = db.Column(db.Integer)
    world_day = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    status = db.Column(db.String(16))

    action = db.Column(db.String(16))

    def __init__(self, county_id, target_id, world_day, duration, action="Unknown"):

        self.county_id = county_id
        self.target_id = target_id
        self.world_day = world_day
        self.duration = duration
        self.status = "Pending"

        self.action = action
