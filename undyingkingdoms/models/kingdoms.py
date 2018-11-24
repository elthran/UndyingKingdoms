from random import choice

from sqlalchemy import orm

from undyingkingdoms.models.achievements import Achievement
from undyingkingdoms.models.users import User
from undyingkingdoms.models.counties import County
from undyingkingdoms.models.bases import GameState, db
from undyingkingdoms.static.metadata import kingdom_names


class Kingdom(GameState):

    name = db.Column(db.String(128), nullable=False, unique=True)
    world_id = db.Column(db.Integer, db.ForeignKey('world.id'), nullable=False)
    counties = db.relationship('County', backref='kingdom')
    leader = db.Column(db.Integer)  # county.id of leader

    def __init__(self):
        used_names = set([kingdom.name for kingdom in Kingdom.query.all()])
        try:
            self.name = choice(list(set(kingdom_names)-used_names))
        except IndexError:
            raise Exception("Add more kingdoms")
        self.leader = 0
        self.world_id = 1
        self.chatroom = []

    @orm.reconstructor
    def init_on_load(self):
        self.chatroom = []

    def __repr__(self):
        return '<Kingdom %r (%r)>' % (self.name, self.id)

    def get_votes_needed(self):
        return max(len(self.counties) // 3, 3)

    def get_most_popular_county(self):
        counties = [(county.get_votes_for_self(), county) for county in self.counties]
        return max(counties, key=lambda x: x[0])[1]

    def count_votes(self):
        if self.get_most_popular_county().get_votes_for_self() >= self.get_votes_needed():
            self.leader = self.get_most_popular_county().id
            leader = County.query.filter_by(id=self.leader).first()
            achievement = Achievement(leader.user_id,
                                      "The King is Dead. Long Live the King.",
                                      "Be voted the King during any age of Undying Kingdoms.")
            db.session.add(achievement)
            db.session.commit()

    def get_leader_name(self, county_id):
        return County.query.filter_by(id=county_id).first().name

