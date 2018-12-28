from random import randint

from undyingkingdoms import db
from undyingkingdoms.models.bases import GameEvent


class Infiltration(GameEvent):

    county_id = db.Column(db.Integer, db.ForeignKey('county.id'), nullable=False)
    target_id = db.Column(db.Integer)
    day = db.Column(db.Integer)
    duration = db.Column(db.Integer)

    mission = db.Column(db.String(64))
    peasant = db.Column(db.Integer)
    archer = db.Column(db.Integer)
    soldier = db.Column(db.Integer)
    elite = db.Column(db.Integer)

    def __init__(self, county_id, target_id, day, duration, mission, peasant=0, archer=0, soldier=0, elite=0):

        self.county_id = county_id
        self.target_id = target_id
        self.day = day
        self.duration = duration

        self.mission = mission
        self.peasant = peasant
        self.archer = archer
        self.soldier = soldier
        self.elite = elite

    def get_troop_report(self, county, enemy_county):
        # Add in modifier for thief guilds here
        self.peasant = enemy_county.armies['peasant'].total * randint(50, 200) // 100
        self.archer = enemy_county.armies['archer'].total * randint(50, 200) // 100
        self.soldier = enemy_county.armies['soldier'].total * randint(50, 200) // 100
        self.elite = enemy_county.armies['elite'].total * randint(50, 200) // 100

    def get_report_age(self, day):
        return day - self.day

