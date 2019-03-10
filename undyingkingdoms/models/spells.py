from undyingkingdoms.models.bases import GameEvent, db


class Spell(GameEvent):

    county_id = db.Column(db.Integer)
    target_id = db.Column(db.Integer)
    spell_id = db.Column(db.Integer)
    world_day = db.Column(db.Integer)
    county_day = db.Column(db.Integer)
    name = db.Column(db.String(64))
    duration = db.Column(db.Integer)  # How many game days until the spell ends

    active = db.Column(db.Boolean)  # If the spell is currently in play
    mana_sustain = db.Column(db.Integer)

    def __init__(self, county_id, target_id, world_day, county_day, name, duration=0):

        self.county_id = county_id
        self.target_id = target_id
        self.world_day = world_day
        self.county_day = county_day
        self.name = name
        self.duration = duration

        self.active = False
        self.mana_sustain = 0

