from undyingkingdoms.models.bases import GameState, db


class Kingdom(GameState):

    name = db.Column(db.String(128), nullable=False)
    counties = db.relationship('County', backref='kingdom')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Kingdom %r (%r)>' % (self.name, self.id)

