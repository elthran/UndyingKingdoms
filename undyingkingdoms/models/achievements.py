from undyingkingdoms import db
from undyingkingdoms.models.bases import GameEvent


class Achievement(GameEvent):

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    category_name = db.Column(db.String(64))
    description = db.Column(db.String(64))
    current_progress = db.Column(db.Integer)
    current_tier = db.Column(db.Integer)
    maximum_tier = db.Column(db.Integer)
    points_rewarded = db.Column(db.Integer)

    land = db.Column(db.Boolean)
    population = db.Column(db.Boolean)
    gold = db.Column(db.Boolean)
    wood = db.Column(db.Boolean)
    iron = db.Column(db.Boolean)
    happiness = db.Column(db.Boolean)
    hunger = db.Column(db.Boolean)

    tier1 = db.Column(db.Integer)
    tier2 = db.Column(db.Integer)
    tier3 = db.Column(db.Integer)
    tier4 = db.Column(db.Integer)
    tier5 = db.Column(db.Integer)

    def __init__(self, category_name, description, points_rewarded, maximum_tier=0,
                 tier1=None,
                 tier2=None,
                 tier3=None,
                 tier4=None,
                 tier5=None,
                 land=False,
                 population=False,
                 gold=False,
                 wood=False,
                 iron=False,
                 happiness=False,
                 hunger=False):
        self.category_name = category_name
        self.description = description
        self.progress = 0
        self._progress_required = None
        self.current_tier = 0
        self.maximum_tier = maximum_tier
        self.points_rewarded = points_rewarded

        self.land = land
        self.population = population
        self.gold = gold
        self.wood = wood
        self.iron = iron
        self.happiness = happiness
        self.hunger = hunger

        self.tier1 = tier1
        self.tier2 = tier2
        self.tier3 = tier3
        self.tier4 = tier4
        self.tier5 = tier5

    @property
    def progress_required(self):
        return self.tiers

    def get_earned_required_amount_message(self):
        if self.current_tier == 0:
            return "You have made no progress on this achievement."
        return "Last reward at {} {}.".format(getattr(self, "tier" + str(self.current_tier)), self.category_name)

    def get_next_required_amount_message(self):
        if self.current_tier == self.maximum_tier:
            return "You have unlocked all tiers."
        return "Next reward at {} {}.".format(getattr(self, "tier" + str(self.current_tier + 1)), self.category_name)
