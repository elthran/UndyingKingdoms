from extensions import flask_db as db
from .bases import GameState


class Army(GameState):
    # These would work better as integers but I'd have to modify a lot of code.
    PEASANT = 0
    SOLDIER = 1
    ARCHER = 2
    BESIEGER = 3
    ELITE = 4
    MONSTER = 5
    SUMMON = 6
    TYPES = dict(peasant=PEASANT, soldier=SOLDIER, archer=ARCHER, besieger=BESIEGER, elite=ELITE, monster=MONSTER, summon=SUMMON)

    county_id = db.Column(db.Integer, db.ForeignKey('county.id', ondelete="CASCADE"), nullable=False)
    name = db.Column(db.String(64))
    class_name = db.Column(db.String(64))
    class_name_plural = db.Column(db.String(64))
    total = db.Column(db.Integer)
    traveling = db.Column(db.Integer)
    currently_training = db.Column(db.Integer)
    trainable_per_day = db.Column(db.Integer)
    gold = db.Column(db.Integer)
    wood = db.Column(db.Integer)
    iron = db.Column(db.Integer)
    upkeep = db.Column(db.Integer)
    category = db.Column(db.String(32))
    attack = db.Column(db.Integer)
    defence = db.Column(db.Integer)
    _health = db.Column(db.Integer)
    armour_type = db.Column(db.String(32))
    description = db.Column(db.String(128))
    ability = db.Column(db.String(32))
    ability_description = db.Column(db.String(128))

    @property
    def type(self):
        """Return an int representing the unit type.

        This will later allow comparison with constants such as:
        if unit.type == unit.BESIEGER:
           do_something_to_siege_units()

        This helps prevent typos.
        """
        return self.TYPES[self.name]

    @property
    def key(self):
        return self.name

    def __init__(self, name, class_name, class_name_plural, total, trainable_per_day, gold, wood, iron, upkeep,
                 category, attack, defence, health, armour_type, description, ability, ability_description):
        self.name = name
        self.class_name = class_name
        self.class_name_plural = class_name_plural
        self.total = total
        self.traveling = 0
        self.currently_training = 0
        self.trainable_per_day = trainable_per_day  # Number than can train per game-day
        self.gold = gold
        self.wood = wood
        self.iron = iron
        self.upkeep = upkeep
        self.category = category
        self.attack = attack
        self.defence = defence
        self.health = health
        self.armour_type = armour_type
        self.description = description
        self.ability = ability
        self.ability_description = ability_description

    @property
    def available(self):
        return self.total - self.traveling

    @property
    def health(self):
        """Health can't go below 0."""
        return max(self._health, 1)

    @health.setter
    def health(self, value):
        self._health = value
