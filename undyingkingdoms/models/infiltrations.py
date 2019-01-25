from random import randint

from undyingkingdoms.models.bases import GameEvent, db


class Infiltration(GameEvent):

    county_id = db.Column(db.Integer, db.ForeignKey('county.id'), nullable=False)
    target_id = db.Column(db.Integer)
    county_age_in_days = db.Column(db.Integer)
    world_age_in_days = db.Column(db.Integer)
    duration = db.Column(db.Integer)  # How many game days until your thieves return
    mission = db.Column(db.String(64))
    amount_of_thieves = db.Column(db.Integer)
    success = db.Column(db.Boolean)

    # Pilfer
    pilfer_amount = db.Column(db.Integer)

    # Burn crops
    crops_burned = db.Column(db.Integer)

    # Sow distrust
    distrust = db.Column(db.Integer)

    peasant = db.Column(db.Integer)
    archer = db.Column(db.Integer)
    soldier = db.Column(db.Integer)
    elite = db.Column(db.Integer)

    def __init__(self, county_id, target_id, county_age_in_days, world_age_in_days, mission, amount):

        self.county_id = county_id
        self.target_id = target_id
        self.county_age_in_days = county_age_in_days
        self.world_age_in_days = world_age_in_days
        self.mission = mission
        self.amount_of_thieves = amount
        self.success = None
        self.duration = 24

        self.pilfer_amount = 0

        self.peasant = 0
        self.archer = 0
        self.soldier = 0
        self.elite = 0

        self.crops_burned = 0

        self.distrust = 0

    def get_troop_report(self, county, enemy_county, amount_sent):
        if amount_sent == 1:
            inaccuracy = 0.5
        elif amount_sent == 2:
            inaccuracy = 0.3
        elif amount_sent >= 3:
            inaccuracy = 0.1

        peasant_inaccuracy = int(max(enemy_county.armies['peasant'].total * inaccuracy, 10))
        archer_inaccuracy = int(max(enemy_county.armies['archer'].total * inaccuracy, 10))
        soldier_inaccuracy = int(max(enemy_county.armies['soldier'].total * inaccuracy, 10))
        elite_inaccuracy = int(max(enemy_county.armies['elite'].total * inaccuracy, 10))

        self.peasant = max(enemy_county.armies['peasant'].total + randint(-peasant_inaccuracy, peasant_inaccuracy), 0)
        self.archer = max(enemy_county.armies['archer'].total + randint(-archer_inaccuracy, archer_inaccuracy), 0)
        self.soldier = max(enemy_county.armies['soldier'].total + randint(-soldier_inaccuracy, soldier_inaccuracy), 0)
        self.elite = max(enemy_county.armies['elite'].total + randint(-elite_inaccuracy, elite_inaccuracy), 0)

    def get_report_age(self, day):
        return day - self.world_age_in_days
