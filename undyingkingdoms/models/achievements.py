from extensions import flask_db as db
from undyingkingdoms.models.bases import GameEvent


class Achievement(GameEvent):

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    name = db.Column(db.String(64))  # Unique name for mapping purposes
    display_title = db.Column(db.String(64))  # The name of the achievement the user sees
    category = db.Column(db.String(64))  # A way to group it for coding purposes
    sub_category = db.Column(db.String(64))  # A way to identify it from its group
    description = db.Column(db.String(64))  # For the user to read
    current_tier = db.Column(db.Integer)  # What level they are on. Starts at 0
    maximum_tier = db.Column(db.Integer)  # The highest level they can reach
    points_rewarded = db.Column(db.Integer)  # Points rewarded at each level

    tier1 = db.Column(db.Integer)
    tier2 = db.Column(db.Integer)
    tier3 = db.Column(db.Integer)
    tier4 = db.Column(db.Integer)
    tier5 = db.Column(db.Integer)

    def __init__(self, name, display_title=None, category=None, sub_category=None, description=None, points_rewarded=0,
                 maximum_tier=0, tier1=None, tier2=None, tier3=None, tier4=None, tier5=None):
        self.name = name
        self.display_title = display_title
        self.category = category
        self.sub_category = sub_category
        self.description = description
        self.current_tier = 0
        self.maximum_tier = maximum_tier
        self.points_rewarded = points_rewarded

        self.tier1 = tier1
        self.tier2 = tier2
        self.tier3 = tier3
        self.tier4 = tier4
        self.tier5 = tier5

    def get_earned_required_amount_message(self):
        if self.current_tier == 0:
            return "You have made no progress on this achievement."
        return f"Last reward at {getattr(self, 'tier' + str(self.current_tier))} {self.name}."

    def get_next_required_amount_message(self):
        if self.current_tier == self.maximum_tier:
            return "You have unlocked all tiers."
        return f"Next reward at {getattr(self, 'tier' + str(self.current_tier + 1))} {self.name}."
