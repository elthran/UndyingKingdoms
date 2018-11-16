from random import choice

from undyingkingdoms.models.bases import GameState, db
from undyingkingdoms.static.metadata import kingdom_names


class Kingdom(GameState):

    name = db.Column(db.String(128), nullable=False, unique=True)
    counties = db.relationship('County', backref='kingdom')
    age = db.Column(db.Integer)
    leader = db.Column(db.Integer)  # county.id of leader

    def __init__(self):
        used_names = set([kingdom.name for kingdom in Kingdom.query.all()])
        try:
            self.name = choice(list(set(kingdom_names)-used_names))
        except IndexError:
            raise Exception("Add more kingdoms")
        self.age = 0
        self.leader = None

    def __repr__(self):
        return '<Kingdom %r (%r)>' % (self.name, self.id)

    def get_votes_needed(self):
        return max(len(self.counties) // 3, 5)

    def get_most_popular_county(self):
        counties = [(county.votes, county) for county in self.counties]
        return max(counties, key=lambda x: x[0])[1]

