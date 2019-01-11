from undyingkingdoms.models.bases import GameEvent, db


class Expedition(GameEvent):

    county_id = db.Column(db.Integer, db.ForeignKey('county.id'), nullable=False)
    duration = db.Column(db.Integer)
    land_acquired = db.Column(db.Integer)

    peasant = db.Column(db.Integer)
    archer = db.Column(db.Integer)
    soldier = db.Column(db.Integer)
    elite = db.Column(db.Integer)

    def __init__(self, county_id, duration, land_acquired=0, peasant=0, archer=0, soldier=0, elite=0):

        self.county_id = county_id
        self.duration = duration
        self.land_acquired = land_acquired

        self.peasant = peasant
        self.archer = archer
        self.soldier = soldier
        self.elite = elite

