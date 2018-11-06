from random import choice

from undyingkingdoms.models.bases import GameState, db
from undyingkingdoms.static.metadata import kingdom_names


class Kingdom(GameState):

    name = db.Column(db.String(128), nullable=False, unique=True)
    counties = db.relationship('County', backref='kingdom')

    def __init__(self):
        used_names = set([kingdom.name for kingdom in Kingdom.query.all()])
        try:
            self.name = choice(list(set(kingdom_names)-used_names))
        except IndexError:
            raise Exception("Add more kingdoms")

    def __repr__(self):
        return '<Kingdom %r (%r)>' % (self.name, self.id)

