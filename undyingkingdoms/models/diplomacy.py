from .bases import GameEvent, db


class Diplomacy(GameEvent):
    # statuses
    CANCELLED = 0
    IN_PROGRESS = 1
    PENDING = 2
    COMPLETED = 3
    WON = 4
    LOST = 5

    # actions
    UNKNOWN = -1
    ALLIANCE = 0
    WAR = 1
    PEACE = 2
    ARMISTACE = 3

    kingdom_id = db.Column(db.Integer, db.ForeignKey('kingdom.id'), nullable=False)
    kingdom = db.relationship('Kingdom', foreign_keys=[kingdom_id])
    target_id = db.Column(db.Integer, db.ForeignKey('kingdom.id'), nullable=False)
    target_kingdom = db.relationship('Kingdom', foreign_keys=[target_id])

    world_day = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    status = db.Column(db.Integer)
    action = db.Column(db.Integer)

    # War
    attacker_current = db.Column(db.Integer)
    defender_current = db.Column(db.Integer)
    attacker_goal = db.Column(db.Integer)
    defender_goal = db.Column(db.Integer)

    def __init__(self, kingdom, target, duration=None, action=UNKNOWN, status=PENDING):
        world = kingdom.world

        self.kingdom = kingdom
        self.target_kingdom = target
        self.world_day = world.day
        self.duration = duration

        self.action = action
        self.status = status

        self.attacker_current = 0
        self.defender_current = 0
        self.attacker_goal = 0
        self.defender_goal = 0

    def get_other_kingdom(self, kingdom):
        """Return the other kingdom involved in this relationship."""
        return self.target_kingdom if self.kingdom_id == kingdom.id else self.kingdom
