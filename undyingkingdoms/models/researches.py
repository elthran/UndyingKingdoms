from undyingkingdoms.models.bases import GameEvent, db


class Research(GameEvent):

    county_id = db.Column(db.Integer, db.ForeignKey('county.id'), nullable=False)
    world_day = db.Column(db.Integer)  # Day you started to reearch
    county_day = db.Column(db.Integer)
    name = db.Column(db.String(64))
    current = db.Column(db.Integer)
    required = db.Column(db.Integer)
    completed = db.Column(db.Boolean)

    def __init__(self, county_id, world_day, county_day, name, required):

        self.county_id = county_id
        self.world_day = world_day
        self.county_day = county_day
        self.name = name
        self.required = required
