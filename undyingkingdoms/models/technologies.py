from undyingkingdoms.models.bases import GameEvent, db


class Technology(GameEvent):
    county_id = db.Column(db.Integer, db.ForeignKey('county.id', ondelete="CASCADE"), nullable=False)
    world_day = db.Column(db.Integer)  # Day you started to reearch
    county_day = db.Column(db.Integer)
    name = db.Column(db.String(64))
    current = db.Column(db.Integer)
    required = db.Column(db.Integer)
    tier = db.Column(db.Integer)
    level = db.Column(db.Integer)
    max_level = db.Column(db.Integer)
    completed = db.Column(db.Boolean)
    description = db.Column(db.String(128))

    def __init__(self, name, required, tier, max_level, description):

        self.world_day = None
        self.county_day = None
        self.name = name
        self.current = 0
        self.required = required
        self.tier = tier
        self.level = 0
        self.max_level = max_level
        self.completed = False
        self.description = description
