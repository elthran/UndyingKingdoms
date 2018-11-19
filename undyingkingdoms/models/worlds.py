import datetime

from undyingkingdoms.models.counties import County
from undyingkingdoms.models.bases import GameState, db


class World(GameState):

    kingdoms = db.relationship('Kingdom', backref='world')
    age = db.Column(db.Integer)  # How many 'reset events'
    day = db.Column(db.Integer)  # How many in-game days have passed this age
    game_clock = db.Column(db.Integer)

    def __init__(self):
        self.age = 0
        self.day = 0
        self.game_clock = datetime.datetime.now().hour

    def check_clock(self):
        now = datetime.datetime.now().hour
        while now != self.game_clock:
            self.advance_day()
            self.game_clock = (self.game_clock + 1) % 24
            db.session.commit()

    def advance_day(self):
        for county in County.query.all():
            county.advance_day()
        self.day += 1

    def advance_age(self):
        self.age += 1

    def __repr__(self):
        return '<World %r (%r)>' % (self.name, self.id)


