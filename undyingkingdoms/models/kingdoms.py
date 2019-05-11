from .notifications import Notification
from .achievements import Achievement
from .counties.exports import County
from .diplomacy import Diplomacy
from .bases import GameState, db


def active_ally_condition(id_join):
    return (
        f"and_("
        f"{id_join}, "
        f"diplomacy.c.status=={Diplomacy.IN_PROGRESS}, "
        f"diplomacy.c.action=={Diplomacy.ALLIANCE}"
        ")"
    )


def pending_ally_condition(id_join):
    return (
        f"and_("
        f"{id_join}, "
        f"diplomacy.c.status=={Diplomacy.PENDING}, "
        f"diplomacy.c.action=={Diplomacy.ALLIANCE}"
        ")"
    )


def war_condition(id_join):
    return (
        f"and_("
        f"{id_join}, "
        f"diplomacy.c.status=={Diplomacy.IN_PROGRESS}, "
        f"diplomacy.c.action=={Diplomacy.WAR}"
        ")"
    )


def armistice_condition(id_join):
    return (
        "and_("
        f"{id_join},"
        f"diplomacy.c.status=={Diplomacy.IN_PROGRESS},"
        f"diplomacy.c.action=={Diplomacy.ARMISTACE}"
        ")"
    )


class Kingdom(GameState):
    name = db.Column(db.String(128), nullable=False, unique=True)
    world_id = db.Column(db.Integer, db.ForeignKey('world.id'), nullable=False)
    clan = db.Column(db.Boolean)
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

    # I'm not sure why this can't be much less complex.
    _armistices_left = db.relationship(
        "Kingdom",
        secondary='diplomacy',
        primaryjoin=armistice_condition("Kingdom.id==diplomacy.c.kingdom_id"),
        secondaryjoin=armistice_condition("Kingdom.id==diplomacy.c.target_id"),
        backref="_armistices_right"
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
    def armistices(self):
        return self._armistices_left + self._armistices_right

    @property
    def total_land_of_top_three_counties(self):
        counties = sorted(self.counties, key=lambda x: x.land, reverse=True)
        return sum(county.land for county in counties[:3])

    def __init__(self, name):
        self.name = name
        self.clan = False
        self.leader = 0
        self.approval_rating = None
        self.world_id = 1
        self.wars_total_lt = 0
        self.wars_won_lt = 0
        self.wars_total_ta = 0
        self.wars_won_ta = 0

    def __repr__(self):
        return '<Kingdom %r (%r)>' % (self.name, self.id)

    def advance_day(self):
        alliances = Diplomacy.query.filter_by(
            kingomd_id=self.id,
            status=Diplomacy.IN_PROGRESS,
            action=Diplomacy.ALLIANCE,
        ).all()
        for alliance in alliances:
            alliance.duration -= 1
            if alliance.duration == 0:
                alliance.status = Diplomacy.COMPLETED

    def get_votes_needed(self):
        return max(len(self.counties) // 3, 3)

    def get_most_popular_county(self):
        counties = [(county.preferences.get_votes_for_self(), county) for county in self.counties if
                    not county.user.is_bot]
        return max(counties, key=lambda x: x[0])[1]

    def count_votes(self):
        county = self.get_most_popular_county()
        preferences = county.preferences
        if preferences.get_votes_for_self() >= self.get_votes_needed():
            self.leader = county.id
            self.approval_rating = 60
            achievement = Achievement.query.filter_by(
                user_id=county.user_id,
                category="class_leader",
                sub_category=county.race.lower()
            ).first()
            if achievement:  # This should be unneeded and SHOULD be throwing errors. But while it's in beta we can leave it in
                achievement.current_tier += 1
            notification = Notification(
                county,
                "Leader",
                "You have been crowned ruler of this kingdom!"
            )
            notification.save()

    @staticmethod
    def get_leader_name(county_id):
        return County.query.get(county_id).name

    def kingdom_button(self, direction, current_id):
        all_kingdoms = Kingdom.query.all()
        eligible_kingdoms = [kingdom for kingdom in all_kingdoms if len(kingdom.counties) > 0]
        eligible_kingdoms = sorted(eligible_kingdoms, key=lambda x: x.id)
        currently_viewing = Kingdom.query.get(current_id)
        current_index = eligible_kingdoms.index(currently_viewing)
        if len(eligible_kingdoms) == 1:
            return eligible_kingdoms[0].id
        if direction == 'left':
            if current_index == 0:
                return eligible_kingdoms[-1].id
            return eligible_kingdoms[current_index - 1].id
        elif direction == 'right':
            if current_index == len(eligible_kingdoms) - 1:
                return eligible_kingdoms[0].id
            return eligible_kingdoms[current_index + 1].id

    def get_land_sum(self):
        return sum(county.land for county in self.counties)

    def declare_war_against(self, enemy):
        war = Diplomacy(self, enemy, action=Diplomacy.WAR, status=Diplomacy.IN_PROGRESS)
        war.attacker_goal = self.get_land_sum() // 10
        war.defender_goal = enemy.get_land_sum() // 10
        war.save()
        self.cancel_alliances(enemy)
        for enemy_county in enemy.counties:
            notice = Notification(
                enemy_county,
                "War",
                f"{self.name} has declared war on you",
                "War"
            )
            notice.save()
        for friendly_county in self.counties:
            notice = Notification(
                friendly_county,
                "War",
                f"We have declared war on {enemy.name}",
                "War"
            )
            notice.save()
        return war

    def cancel_alliances(self, enemy):
        pending_alliance = self.relations_query(enemy).filter_by(
            status=Diplomacy.PENDING, action=Diplomacy.ALLIANCE
        ).first()
        if pending_alliance:
            pending_alliance.status = Diplomacy.CANCELLED

    def war_won_against(self, enemy):
        for county in self.counties:
            notice = Notification(county, "War", f"We have won the war against {enemy.name}!", "War")
            notice.save()
        for county in enemy.counties:
            notice = Notification(county, "War", f"We have lost the war against {self.name}!", "War")
            notice.save()
        self.wars_won_ta += 1
        self.wars_won_lt += 1

        armistace = Diplomacy(self, enemy, action=Diplomacy.ARMISTACE, status=Diplomacy.IN_PROGRESS)
        armistace.duration = 24
        armistace.save()

    def get_war(self, target):
        """Get war between this kingdom given a target, if it exists."""
        war = self.relations_query(target).filter_by(action=Diplomacy.WAR, status=Diplomacy.IN_PROGRESS).first()
        return war

    def update_war_status(self, war, target):
        """Check whether a war is won and if so update status."""
        # this kingdom is aggressor
        if war.kingdom_id == self.id:
            if war.attacker_current >= war.attacker_goal:
                self.war_won_against(target)
                war.status = Diplomacy.WON
        else:  # this kingdom is defender
            if war.defender_current >= war.defender_goal:
                target.war_won_against(self)
                war.status = Diplomacy.LOST

    def relations_query(self, target):
        """Get all diplomacy relationships between this and another kingdom.

        You can then filter this for to get an active war via:

        war = self.relations_query(target).filter_by(action=Diplomacy.WAR, status=Diplomacy.IN_PROGRESS).first()
        """
        return Diplomacy.query.filter(
            (Diplomacy.kingdom_id == self.id &
             Diplomacy.target_id == target.id) |
            (Diplomacy.kingdom_id == target.id &
             Diplomacy.target_id == self.id)
        )
