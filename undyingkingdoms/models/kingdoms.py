from undyingkingdoms.models.notifications import Notification
from undyingkingdoms.models.achievements import Achievement
from undyingkingdoms.models.counties import County
from undyingkingdoms.models.diplomacy import Diplomacy
from undyingkingdoms.models.bases import GameState, db
from undyingkingdoms.static.metadata.metadata import kingdom_names


def active_ally_condition(id_join):
    return (
        f"and_("
        f"{id_join}, "
        "diplomacy.c.status=='In Progress', "
        "diplomacy.c.action=='Alliance'"
        ")"
    )


def pending_ally_condition(id_join):
    return (
        f"and_("
        f"{id_join}, "
        "diplomacy.c.status=='Pending', "
        "diplomacy.c.action=='Alliance'"
        ")"
    )


def war_condition(id_join):
    return (
        f"and_("
        f"{id_join}, "
        "diplomacy.c.status=='In Progress', "
        "diplomacy.c.action=='War'"
        ")"
    )


class Kingdom(GameState):
    name = db.Column(db.String(128), nullable=False, unique=True)
    world_id = db.Column(db.Integer, db.ForeignKey('world.id'), nullable=False)
    counties = db.relationship('County', backref='kingdom')
    leader = db.Column(db.Integer)  # county.id of leader
    approval_rating = db.Column(db.Integer)  # How well liked the leader is
    wars_total_lt = db.Column(db.Integer)
    wars_won_lt = db.Column(db.Integer)
    wars_total_ta = db.Column(db.Integer)
    wars_won_ta = db.Column(db.Integer) 

    _kingdoms_you_allied_with = db.relationship(
        'Kingdom',
        secondary="diplomacy",
        primaryjoin=active_ally_condition("Kingdom.id==diplomacy.c.kingdom_id"),
        secondaryjoin=active_ally_condition("Kingdom.id==diplomacy.c.target_id"),
        backref="_kingdoms_that_allied_with_you"
    )

    _kingdoms_you_started_wars_with = db.relationship(
        'Kingdom',
        secondary='diplomacy',
        primaryjoin=war_condition("Kingdom.id==diplomacy.c.kingdom_id"),
        secondaryjoin=war_condition("Kingdom.id==diplomacy.c.target_id"),
        backref="_kingdoms_that_started_wars_with_you"
    )

    _pending_alliances_you_started = db.relationship(
        'Diplomacy',
        primaryjoin=pending_ally_condition("Kingdom.id==diplomacy.c.kingdom_id"),
    )

    _alliances_you_started = db.relationship(
        'Diplomacy',
        primaryjoin=active_ally_condition("Kingdom.id==diplomacy.c.kingdom_id")
    )

    _alliances_started_with_you = db.relationship(
        'Diplomacy',
        primaryjoin=active_ally_condition("Kingdom.id==diplomacy.c.target_id")
    )

    _wars_you_started = db.relationship(
        'Diplomacy',
        primaryjoin=war_condition("Kingdom.id==diplomacy.c.kingdom_id")
    )

    _wars_started_with_you = db.relationship(
        'Diplomacy',
        primaryjoin=war_condition("Kingdom.id==diplomacy.c.target_id")
    )

    _pending_alliances_started_with_you = db.relationship(
        'Diplomacy',
        primaryjoin=active_ally_condition("Kingdom.id==diplomacy.c.target_id"),
    )

    _kingdoms_who_we_offered_alliances = db.relationship(
        'Kingdom',
        secondary='diplomacy',
        primaryjoin=pending_ally_condition("Kingdom.id==diplomacy.c.kingdom_id"),
        secondaryjoin=pending_ally_condition("Kingdom.id==diplomacy.c.target_id"),
        backref="_kingdoms_who_offered_us_alliances"
    )

    @property
    def pending_alliances(self):
        return self._pending_alliances_you_started + self._pending_alliances_started_with_you

    @property
    def alliances(self):
        return self._alliances_you_started + self._alliances_started_with_you

    @property
    def wars(self):
        return self._wars_you_started + self._wars_started_with_you

    @property
    def allies(self):
        return self._kingdoms_you_allied_with + self._kingdoms_that_allied_with_you

    @property
    def enemies(self):
        return self._kingdoms_you_started_wars_with + self._kingdoms_that_started_wars_with_you

    @property
    def kingdoms_who_offered_us_alliances(self):
        return self._kingdoms_who_offered_us_alliances

    @property
    def kingdoms_who_we_offered_alliances_to(self):
        return self._kingdoms_who_we_offered_alliances

    @property
    def kingdoms_with_pending_alliances(self):
        return self._kingdoms_who_offered_us_alliances + self._kingdoms_who_we_offered_alliances

    @property
    def total_land_of_top_three_counties(self):
        counties = sorted(self.counties, key=lambda x: x.land, reverse=True)
        return sum(county.land for county in counties[:3])

    def __init__(self, name):
        self.name = name
        self.leader = 0
        self.approval_rating = 60
        self.world_id = 1
        self.wars_total_lt = 0
        self.wars_won_lt = 0
        self.wars_total_ta = 0
        self.wars_won_ta = 0

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

    def war_won(self, war):
        enemy = war.get_other_kingdom(self)
        for county in self.counties:
            notice = Notification(county.id, "War", "We have won the war against {}!".format(enemy.name), self.world.day, "War")
            notice.save()
        for county in enemy.counties:
            notice = Notification(county.id, "War", "We have lost the war against {}!".format(self.name), self.world.day, "War")
            notice.save()
        self.wars_won_ta += 1
        self.wars_won_lt += 1



