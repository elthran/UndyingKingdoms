from undyingkingdoms.models.bases import GameEvent, db


class Magic(GameEvent):

    county_id = db.Column(db.Integer, db.ForeignKey('county.id'), nullable=False)
    county_day = db.Column(db.Integer)
    name = db.Column(db.String(64))
    category = db.Column(db.String(64))
    known = db.Column(db.Boolean)
    mana_cost = db.Column(db.Integer)
    mana_sustain = db.Column(db.Integer)  # Mana required to spend each day to sustain the spell
    duration = db.Column(db.Integer)  # How many game days the spell lasts for
    description = db.Column(db.String(64))

    def __init__(self, name, category, known, mana_cost, mana_sustain=0, duration=0, description="Unknown"):

        self.name = name
        self.category = category
        self.known = known
        self.mana_cost = mana_cost
        self.mana_sustain = mana_sustain
        self.duration = duration
        self.description = description
