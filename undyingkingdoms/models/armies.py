from random import randint

from extensions import flask_db as db
from undyingkingdoms.calculations.modifiers import get_modifiers
from undyingkingdoms.models.bases import GameState


class Army(GameState):
    county_id = db.Column(db.Integer, db.ForeignKey('county.id', ondelete="CASCADE"), nullable=False)
    name = db.Column(db.String(64))
    class_name = db.Column(db.String(64))
    class_name_plural = db.Column(db.String(64))
    total = db.Column(db.Integer)
    traveling = db.Column(db.Integer)
    currently_training = db.Column(db.Integer)
    trainable_per_day = db.Column(db.Integer)
    gold = db.Column(db.Integer)
    iron = db.Column(db.Integer)
    wood = db.Column(db.Integer)
    upkeep = db.Column(db.Integer)
    attack = db.Column(db.Integer)
    _defence = db.Column(db.Integer)
    health = db.Column(db.Integer)
    description = db.Column(db.String(128))

    def __init__(self, name, class_name, class_name_plural, total, trainable_per_day, gold, iron, wood, upkeep, attack, defence, health, description):
        self.name = name
        self.class_name = class_name
        self.class_name_plural = class_name_plural
        self.total = total
        self.traveling = 0
        self.currently_training = 0
        self.trainable_per_day = trainable_per_day  # Number than can train per game-day
        self.gold = gold
        self.iron = iron
        self.wood = wood
        self.upkeep = upkeep
        self.attack = attack
        self.defence = defence
        self.health = health
        self.description = description

    @property
    def available(self):
        return self.total - self.traveling

    @property
    def defence(self):
        bonuses = 1
        try:
            bonuses = get_modifiers(self.county, 'unit_defence', self.name)  # County, Defence, Unit Name
        except AttributeError:
            pass
        return self._defence + bonuses

    @defence.setter
    def defence(self, value):
        self._defence = value
