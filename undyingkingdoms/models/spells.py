from random import randint

from undyingkingdoms.models.bases import GameEvent, db


class Spell(GameEvent):

    county_id = db.Column(db.Integer, db.ForeignKey('county.id'), nullable=False)
    target_id = db.Column(db.Integer)
    world_day = db.Column(db.Integer)
    county_day = db.Column(db.Integer)
    name = db.Column(db.String(64))
    category = db.Column(db.String(64))
    mana_cost = db.Column(db.Integer)
    mana_sustain = db.Column(db.Integer)  # Mana required to spend each day to sustain the spell
    duration = db.Column(db.Integer)  # How many game days until the spell ends

    def __init__(self, name, category, mana_cost, mana_sustain=0, duration=0):

        self.name = name
        self.category = category
        self.mana_cost = mana_cost
        self.mana_sustain = mana_sustain
        self.duration = duration
