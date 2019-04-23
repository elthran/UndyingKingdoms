from random import randint

from undyingkingdoms.models.bases import GameEvent, db
from .effects import Effect


class Casting(GameEvent):
    county_id = db.Column(db.Integer, db.ForeignKey('county.id'))
    target_id = db.Column(db.Integer, db.ForeignKey('county.id'))
    target_relation = db.Column(db.String(16))
    spell_id = db.Column(db.Integer)
    world_day = db.Column(db.Integer)
    county_day = db.Column(db.Integer)
    success = db.Column(db.Boolean)
    output = db.Column(db.Float)
    name = db.Column(db.String(64))
    display_name = db.Column(db.String(64))
    duration = db.Column(db.Integer)  # How many game days until the spell ends

    active = db.Column(db.Boolean)  # If the spell is currently in play
    mana_sustain = db.Column(db.Integer)

    # consider passing in spell and country objects
    # as this will make execute more efficient.
    def __init__(self, county_id, target_id, spell_id, world_day, county_day, name,
                 display_name, duration=0, target_relation="Unknown", output=0):

        self.county_id = county_id
        self.target_id = target_id
        self.spell_id = spell_id
        self.target_relation = target_relation
        self.world_day = world_day
        self.county_day = county_day
        self.name = name
        self.display_name = display_name
        self.duration = duration
        self.success = True
        self.output = output

        self.active = False
        self.mana_sustain = 0

    def activate(self, spell, county, target):
        """Attempt to cast the spell."""

        # spell should still cost event if not successful?
        effect = Effect(spell, self, county, target)

        # check if spell fails
        if target.chance_to_disrupt_spell() > randint(1, 100) and self.target_relation == 'hostile':
            self.success = False
            self.duration = 0
            self.active = False
            return False  # casting failure

        effect.execute()

        self.handle_war(county, spell, target)
        return True  # casting successful

    def handle_war(self, county, spell, target):
        """Check if war points should be awarded."""
        if self.target_relation == 'hostile':
            kingdom = county.kingdom
            war = kingdom.get_war(target)
            if war:
                if war.kingdom_id == kingdom.id:
                    war.attacker_current += spell.mana_cost // 2
                else:
                    war.defender_current += spell.mana_cost // 2
                kingdom.update_war_status(war, target)

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
