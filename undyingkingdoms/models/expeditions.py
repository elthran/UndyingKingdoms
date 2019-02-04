from undyingkingdoms.models.bases import GameEvent, db


class Expedition(GameEvent):

    county_id = db.Column(db.Integer, db.ForeignKey('county.id'), nullable=False)
    target_id = db.Column(db.Integer)
    day = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    land_acquired = db.Column(db.Integer)
    mission = db.Column(db.String(64))

    peasant = db.Column(db.Integer)
    soldier = db.Column(db.Integer)
    elite = db.Column(db.Integer)
    monster = db.Column(db.Integer)

    def __init__(self, county_id, target_id, county_age_in_days, world_age_in_days, duration, mission, land_acquired=0, peasant=0, soldier=0, elite=0, monster=0):

        self.county_id = county_id
        self.target_id = target_id
        self.county_age_in_days = county_age_in_days
        self.world_age_in_days = world_age_in_days
        self.duration = duration
        self.land_acquired = land_acquired
        self.mission = mission

        self.peasant = peasant
        self.soldier = soldier
        self.elite = elite
        self.monster = monster

