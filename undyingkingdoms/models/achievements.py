from undyingkingdoms import db
from undyingkingdoms.models.bases import GameEvent


class Achievement(GameEvent):

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    category_name = db.Column(db.String(64))
    description = db.Column(db.String(64))
    current_progress = db.Column(db.Integer)
    current_level = db.Column(db.Integer)
    points_rewarded = db.Column(db.Integer)
    land = db.Column(db.Boolean)
    population = db.Column(db.Boolean)
    awarded = db.Column(db.Boolean)

    def __init__(self, category_name, description, points_rewarded,
                 land=False,
                 population=False):
        self.category_name = category_name
        self.description = description
        self.progress = 0
        self._progress_required = None
        self.current_level = 0
        self.points_rewarded = points_rewarded

        self.land = land
        self.population = population

        self.awarded = False

    @property
    def progress_required(self):
        if self.land:
            return [160, 170, 200]
        return [525, 550, 575, 600]

    def display_progress(self):
        return

    def get_max_level(self):
        return len(self.progress_required)

    def check_for_level_up(self):
        pass
