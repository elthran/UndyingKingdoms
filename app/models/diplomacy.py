from sqlalchemy.ext.hybrid import hybrid_property

from .bases import GameEvent, db


class Diplomacy(GameEvent):
    # statuses
    CANCELLED = 0
    IN_PROGRESS = 1
    PENDING = 2
    COMPLETED = 3
    AGGRESSOR_WON = 4
    DEFENDER_WON = 5

    # actions
    UNKNOWN = -1
    ALLIANCE = 0
    WAR = 1
    PEACE = 2
    ARMISTICE = 3

    kingdom_id = db.Column(db.Integer, db.ForeignKey('kingdom.id'), nullable=False)
    kingdom = db.relationship('Kingdom', foreign_keys=[kingdom_id])
    target_id = db.Column(db.Integer, db.ForeignKey('kingdom.id'), nullable=False)
    target_kingdom = db.relationship('Kingdom', foreign_keys=[target_id])

    world_day = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    status = db.Column(db.Integer)
    action = db.Column(db.Integer)

    # War
    aggressor_current = db.Column(db.Integer)
    defender_current = db.Column(db.Integer)
    aggressor_goal = db.Column(db.Integer)
    defender_goal = db.Column(db.Integer)

    @property
    def aggressor(self):
        if self.action == Diplomacy.WAR:
            return self.kingdom
        return None

    @property
    def defender(self):
        if self.action == Diplomacy.WAR:
            return self.target_kingdom
        return None

    def __init__(self, kingdom, target, duration=None, action=UNKNOWN, status=PENDING):
        world = kingdom.world

        self.kingdom = kingdom
        self.target_kingdom = target
        self.world_day = world.day
        self.duration = duration

        self.action = action
        self.status = status

        self.aggressor_current = 0
        self.defender_current = 0
        self.aggressor_goal = 0
        self.defender_goal = 0

    def get_other_kingdom(self, kingdom):
        """Return the other kingdom involved in this relationship."""
        return self.target_kingdom \
            if self.kingdom_id == kingdom.id \
            else self.kingdom

    @hybrid_property
    def war_over(self):
        return self.aggressor_current >= self.aggressor_goal or self.defender_current >= self.defender_goal
