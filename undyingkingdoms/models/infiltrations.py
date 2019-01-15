from random import randint

from extensions import flask_db as db
from undyingkingdoms.models.bases import GameEvent


class Infiltration(GameEvent):

    county_id = db.Column(db.Integer, db.ForeignKey('county.id'), nullable=False)
    user_id = db.Column(db.Integer)
    target_id = db.Column(db.Integer)
    day = db.Column(db.Integer)  # On which game day the report was created
    duration = db.Column(db.Integer)  # How many game days until your thieves return

    mission = db.Column(db.String(64))
    peasant = db.Column(db.Integer)
    archer = db.Column(db.Integer)
    soldier = db.Column(db.Integer)
    elite = db.Column(db.Integer)

    def __init__(self, county_id, user_id, target_id, day, mission, peasant=0, archer=0, soldier=0, elite=0):

        self.county_id = county_id
        self.user_id = user_id
        self.target_id = target_id
        self.day = day
        self.duration = None  # The default is 24 game days for thieves to return

        self.mission = mission
        self.peasant = peasant
        self.archer = archer
        self.soldier = soldier
        self.elite = elite

    def get_troop_report(self, county, enemy_county):
        friendly_guilds = county.buildings['guilds'].total
        enemy_guilds = enemy_county.buildings['guilds'].total
        inaccuracy = max((enemy_guilds * 3) - (friendly_guilds * 2), 1)
        self.peasant = max(enemy_county.armies['peasant'].total + randint(-inaccuracy, inaccuracy), 0)
        self.archer = max(enemy_county.armies['archer'].total + randint(-inaccuracy, inaccuracy), 0)
        self.soldier = max(enemy_county.armies['soldier'].total + randint(-inaccuracy, inaccuracy), 0)
        self.elite = max(enemy_county.armies['elite'].total + randint(-inaccuracy, inaccuracy), 0)

    def get_report_age(self, day):
        return day - self.day

