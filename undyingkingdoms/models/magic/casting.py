from random import randint

from undyingkingdoms.models.bases import GameEvent, db

class Casting(GameEvent):
    county_id = db.Column(db.Integer, db.ForeignKey('county.id'))
    target_id = db.Column(db.Integer, db.ForeignKey('county.id'))
    target_relation = db.Column(db.String(16))
    spell_id = db.Column(db.Integer)
    world_day = db.Column(db.Integer)
    county_day = db.Column(db.Integer)
    success = db.Column(db.Boolean)
    name = db.Column(db.String(64))
    duration = db.Column(db.Integer)  # How many game days until the spell ends

    active = db.Column(db.Boolean)  # If the spell is currently in play
    mana_sustain = db.Column(db.Integer)

    # consider passing in spell and country objects
    # as this will make execute more efficient.
    def __init__(self, county_id, target_id, spell_id, world_day, county_day, name, duration=0, target_relation="Unknown"):

        self.county_id = county_id
        self.target_id = target_id
        self.spell_id = spell_id
        self.target_relation = target_relation
        self.world_day = world_day
        self.county_day = county_day
        self.name = name
        self.duration = duration
        self.success = True

        self.active = False
        self.mana_sustain = 0

    def execute(self, spell, county, target):
        """Attempt to cast the spell."""
        if county.chance_to_cast_spell() < randint(1, 100) or (target.chance_to_disrupt_spell() > randint(1, 100) and self.target_relation == 'hostile'):  # Spell failed to cast
            self.success = False
            self.duration = 0
            self.active = False
            return False  # casting failure

        if spell.category == 'aura':
            self.active = True
            self.mana_sustain = spell.mana_sustain
        county.mana -= spell.mana_cost
        return True  # casting successful

    @staticmethod
    def get_active_spells(county):
        return Casting.query.filter_by(county_id=county.id)\
            .filter((Casting.duration > 0) | (Casting.active==True))\
            .all()

    @staticmethod
    def get_enemy_spells(county):
        return Casting.query.filter_by(target_id=county.id)\
            .filter((Casting.county_id != county.id)
                    & ((Casting.duration > 0)
                    | (Casting.active==True)))\
            .all()

    @staticmethod
    def get_sustain_mana_requirement(county):
        # I suggest making this an SQL query eventually.
        return sum(spell.mana_sustain
                   for spell in Casting.get_active_spells(county))
