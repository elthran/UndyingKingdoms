from undyingkingdoms.models.achievements import Achievement
from undyingkingdoms.models.counties import County
from undyingkingdoms.models.diplomacy import Diplomacy
from undyingkingdoms.models.bases import GameState, db
from undyingkingdoms.static.metadata.metadata import kingdom_names


class Kingdom(GameState):
    name = db.Column(db.String(128), nullable=False, unique=True)
    world_id = db.Column(db.Integer, db.ForeignKey('world.id'), nullable=False)
    counties = db.relationship('County', backref='kingdom')
    leader = db.Column(db.Integer)  # county.id of leader

    def __init__(self, name):
        self.name = name
        self.leader = 0
        self.world_id = 1

    def __repr__(self):
        return '<Kingdom %r (%r)>' % (self.name, self.id)

    def advance_day(self):
        alliances = Diplomacy.query.filter_by(status="In Progress")\
            .filter_by(action="Alliance")\
            .filter(Diplomacy.kingdom_id == self.id).all()
        for alliance in alliances:
            alliance.duration -= 1
            if alliance.duration == 0:
                alliance.action = "Completed"

    def get_votes_needed(self):
        return max(len(self.counties) // 3, 3)

    def get_most_popular_county(self):
        counties = [(county.get_votes_for_self(), county) for county in self.counties if not county.user.is_bot]
        return max(counties, key=lambda x: x[0])[1]

    def count_votes(self):
        if self.get_most_popular_county().get_votes_for_self() >= self.get_votes_needed():
            county = self.get_most_popular_county()
            self.leader = county.id
            achievement = Achievement.query.filter_by(user_id=county.user_id, category="class_leader",
                                                      sub_category=county.race.lower()).first()
            if achievement:  # This should be unneeded and SHOULD be throwing errors. But while it's in beta we can leave it in
                achievement.current_tier += 1

    @staticmethod
    def get_leader_name(county_id):
        return County.query.get(county_id).name

    def kingdom_button(self, direction, current_id):
        if direction == 'left':
            current_id -= 1
        elif direction == 'right':
            current_id += 1
        if current_id == 0:
            current_id = len(kingdom_names)
        elif current_id > len(kingdom_names):
            current_id = 1
        chosen_kingdom = Kingdom.query.get(current_id)  # Get the chosen kingdom
        if len(chosen_kingdom.counties) == 0:  # If it's empty, skip it and go to next kingdom in that direction
            return self.kingdom_button(direction, current_id)
        return current_id

    def get_land_sum(self):
        return sum(county.land for county in self.counties)

    def get_enemies(self):
        kingdom_ids = []
        kingdoms = []
        wars = Diplomacy.query.filter_by(status="In Progress").filter_by(action="War") \
            .filter((Diplomacy.kingdom_id == self.id) | (Diplomacy.target_id == self.id)) \
            .all()
        for war in wars:
            if war.kingdom_id != self.id:
                kingdom_ids.append(war.kingdom_id)
            elif war.target_id != self.id:
                kingdom_ids.append(war.target_id)
        for kingdom_id in kingdom_ids:
            kingdoms.append(Kingdom.query.get(kingdom_id))
        return kingdoms

    def get_allies(self):
        kingdom_ids = []
        kingdoms = []
        alliances = Diplomacy.query.filter_by(status="In Progress").filter_by(action="Alliance") \
            .filter((Diplomacy.kingdom_id == self.id) | (Diplomacy.target_id == self.id)) \
            .all()
        for alliance in alliances:
            if alliance.kingdom_id != self.id:
                kingdom_ids.append(alliance.kingdom_id)
            elif alliance.target_id != self.id:
                kingdom_ids.append(alliance.target_id)
        for kingdom_id in kingdom_ids:
            kingdoms.append(Kingdom.query.get(kingdom_id))
        return kingdoms

    def get_pending_alliance(self, keyword="from"):
        kingdom_ids = []
        kingdoms = []
        if keyword == "from":
            alliances = Diplomacy.query.filter_by(status="Pending").filter_by(action="Alliance").filter(
                Diplomacy.kingdom_id == self.id).all()
            for alliance in alliances:
                kingdom_ids.append(alliance.target_id)
        else:
            alliances = Diplomacy.query.filter_by(status="Pending").filter_by(action="Alliance").filter(
                Diplomacy.target_id == self.id).all()
            for alliance in alliances:
                kingdom_ids.append(alliance.kingdom_id)
        for kingdom_id in kingdom_ids:
            kingdoms.append(Kingdom.query.get(kingdom_id))
        return kingdoms
