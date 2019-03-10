from undyingkingdoms.models.bases import GameEvent, db


class Expedition(GameEvent):

    county_id = db.Column(db.Integer, db.ForeignKey('county.id'), nullable=False)
    target_id = db.Column(db.Integer)
    world_day = db.Column(db.Integer)
    county_day = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    mission = db.Column(db.String(64))

    war_id = db.Column(db.Integer)

    # Results
    success = db.Column(db.Boolean)
    attack_power = db.Column(db.Integer)
    defence_power = db.Column(db.Integer)
    
    land_acquired = db.Column(db.Integer)

    land_razed = db.Column(db.Integer)
    
    gold_gained = db.Column(db.Integer)
    wood_gained = db.Column(db.Integer)
    iron_gained = db.Column(db.Integer)

    # Troops remaining
    peasant = db.Column(db.Integer)
    soldier = db.Column(db.Integer)
    elite = db.Column(db.Integer)
    monster = db.Column(db.Integer)

    # Troops sent (for analytics)
    peasant_sent = db.Column(db.Integer)
    soldier_sent = db.Column(db.Integer)
    elite_sent = db.Column(db.Integer)
    monster_sent = db.Column(db.Integer)

    def __init__(self, county_id, target_id, world_day, county_day, attack_power=0, defence_power=0, mission="Unknown",
                 land_acquired=0, land_razed=0, gold_gained=0, wood_gained=0, iron_gained=0, peasant=0, soldier=0, elite=0, monster=0,
                 peasant_sent=0, soldier_sent=0, elite_sent=0, monster_sent=0):

        self.county_id = county_id
        self.target_id = target_id
        self.world_day = world_day
        self.county_day = county_day
        self.attack_power = attack_power
        self.defence_power = defence_power
        self.mission = mission

        self.war_id = 0

        self.land_acquired = land_acquired

        self.land_razed = land_razed
        
        self.gold_gained = gold_gained
        self.wood_gained = wood_gained
        self.iron_gained = iron_gained

        self.peasant = peasant
        self.soldier = soldier
        self.elite = elite
        self.monster = monster

        self.peasant_sent = peasant_sent
        self.soldier_sent = soldier_sent
        self.elite_sent = elite_sent
        self.monster_sent = monster_sent

