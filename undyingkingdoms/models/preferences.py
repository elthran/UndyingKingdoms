from datetime import datetime

from undyingkingdoms.models.bases import GameState, db


class Preferences(GameState):
    county_id = db.Column(db.Integer, db.ForeignKey('county.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    tax_rate = db.Column(db.Integer)
    rations = db.Column(db.Float)
    production_choice = db.Column(db.Integer)
    research_choice = db.Column(db.String(128))

    last_checked_townhall = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, county_id, user_id):
        self.county_id = county_id
        self.user_id = user_id
        self.tax_rate = 8
        self.rations = 1
        self.production_choice = 0
        self.research_choice = 'agriculture'

