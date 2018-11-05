from random import choice

from undyingkingdoms.models.bases import GameState, db
from undyingkingdoms.static.metadata import kingdom_names


class Kingdom(GameState):

    name = db.Column(db.String(128), nullable=False, unique=True)
    counties = db.relationship('County', backref='kingdom')

    def __init__(self):
        # This should randomly choose one from kingdom_names but without choosing one that has been used.
        # Right now it will crash the database if two kingdoms are chosen with duplicate names.
        self.name = choice(kingdom_names)

    def __repr__(self):
        return '<Kingdom %r (%r)>' % (self.name, self.id)

