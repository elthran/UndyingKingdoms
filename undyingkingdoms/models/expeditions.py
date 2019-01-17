from undyingkingdoms.models.bases import GameEvent, db


class Expedition(GameEvent):

    county_id = db.Column(db.Integer, db.ForeignKey('county.id'), nullable=False)
    user_id = db.Column(db.Integer)
    day = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    land_acquired = db.Column(db.Integer)

    mission = db.Column(db.String(64))
    peasant = db.Column(db.Integer)
    archer = db.Column(db.Integer)
    soldier = db.Column(db.Integer)
    elite = db.Column(db.Integer)

    def __init__(self, county_id, user_id, day, duration, mission, land_acquired=0, peasant=0, archer=0, soldier=0, elite=0):

        self.county_id = county_id
        self.user_id = user_id
        self.day = day
        self.duration = duration
        self.land_acquired = land_acquired

        self.mission = mission
        self.peasant = peasant
        self.archer = archer
        self.soldier = soldier
        self.elite = elite

