from random import randint

from .bases import GameEvent, db


class Infiltration(GameEvent):

    county_id = db.Column(db.Integer, db.ForeignKey('county.id'), nullable=False)
    target_id = db.Column(db.Integer, db.ForeignKey('county.id'), nullable=False)
    world_day = db.Column(db.Integer)
    county_day = db.Column(db.Integer)
    duration = db.Column(db.Integer)  # How many game days until your thieves return
    mission = db.Column(db.String(64))
    amount_of_thieves = db.Column(db.Integer)
    success = db.Column(db.Boolean)
    # Pilfer
    pilfer_amount = db.Column(db.Integer)
    # Burn crops
    crops_burned = db.Column(db.Integer)
    # Pastures destroyed
    dairy_destroyed = db.Column(db.Integer)
    # Sow distrust
    distrust = db.Column(db.Integer)
    # Steal Research
    research_stolen = db.Column(db.Integer)
    # Scout military
    peasant = db.Column(db.Integer)
    archer = db.Column(db.Integer)
    soldier = db.Column(db.Integer)
    besieger = db.Column(db.Integer)
    summon = db.Column(db.Integer)
    elite = db.Column(db.Integer)
    fort = db.Column(db.Integer)

    def __init__(self, county_id, target_id, world_day, county_day, mission, amount):

        self.county_id = county_id
        self.target_id = target_id
        self.world_day = world_day
        self.county_day = county_day
        self.mission = mission
        self.amount_of_thieves = amount
        self.success = None
        self.duration = 24

        self.peasant = 0
        self.archer = 0
        self.soldier = 0
        self.besieger = 0
        self.summon = 0
        self.elite = 0
        
        self.fort = 0

        self.crops_burned = 0
        self.dairy_destroyed = 0
        self.pilfer_amount = 0
        self.distrust = 0
        self.research_stolen = 0

    def get_troop_report(self, county, enemy_county, amount_sent):
        enemy_infrastructure = enemy_county.infrastructure
        if amount_sent == 1:
            inaccuracy = 1.0
        elif amount_sent == 2:
            inaccuracy = 0.75
        elif amount_sent >= 3:
            inaccuracy = 0.5

        peasant_inaccuracy = int(max(enemy_county.armies['peasant'].total * inaccuracy, 2))
        archer_inaccuracy = int(max(enemy_county.armies['archer'].total * inaccuracy, 2))
        soldier_inaccuracy = int(max(enemy_county.armies['soldier'].total * inaccuracy, 2))
        besieger_inaccuracy = int(max(enemy_county.armies['besieger'].total * inaccuracy, 2))
        summon_inaccuracy = int(max(enemy_county.armies['summon'].total * inaccuracy, 2))
        elite_inaccuracy = int(max(enemy_county.armies['elite'].total * inaccuracy, 2))
        fort_inaccuracy = int(max(enemy_infrastructure.buildings['fort'].total * inaccuracy, 2))

        self.peasant = max(enemy_county.armies['peasant'].total + randint(-peasant_inaccuracy, peasant_inaccuracy), 0)
        self.archer = max(enemy_county.armies['archer'].total + randint(-archer_inaccuracy, archer_inaccuracy), 0)
        self.soldier = max(enemy_county.armies['soldier'].total + randint(-soldier_inaccuracy, soldier_inaccuracy), 0)
        self.besieger = max(enemy_county.armies['besieger'].total + randint(-besieger_inaccuracy, besieger_inaccuracy), 0)
        self.summon = max(enemy_county.armies['summon'].total + randint(-summon_inaccuracy, summon_inaccuracy), 0)
        self.elite = max(enemy_county.armies['elite'].total + randint(-elite_inaccuracy, elite_inaccuracy), 0)
        self.fort = max(enemy_infrastructure.buildings['fort'].total + randint(-fort_inaccuracy, fort_inaccuracy), 0)

    def get_report_age(self, day):
        return day - self.world_day
