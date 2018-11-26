from datetime import datetime, timedelta

from undyingkingdoms.models.users import User
from undyingkingdoms.models import Session, DailyActiveUser
from undyingkingdoms.models.counties import County
from undyingkingdoms.models.bases import GameState, db


class World(GameState):

    kingdoms = db.relationship('Kingdom', backref='world')
    age = db.Column(db.Integer)  # How many 'reset events'
    day = db.Column(db.Integer)  # How many in-game days have passed this age
    game_clock = db.Column(db.Integer)
    analytic_cycles = db.Column(db.Integer)  # Temporary. Will run every 24h once scheduler up

    def __init__(self):
        self.age = 0
        self.day = 0
        self.game_clock = datetime.now().hour
        self.analytic_cycles = 0

    def check_clock(self):
        now = datetime.now().hour
        while now != self.game_clock:
            self.advance_day()
            self.game_clock = (self.game_clock + 1) % 24
            db.session.commit()
        while (self.day // 1) > self.analytic_cycles:
            self.advance_24h_analytics()
            self.analytic_cycles += 1

    def advance_day(self):
        for county in County.query.all():
            county.advance_day()
        self.day += 1

    def advance_age(self):
        self.age += 1

    def advance_24h_analytics(self):
        users = User.query.all()
        for user in users:
            session = DailyActiveUser(user.id, self.day)
            db.session.add(session)
            db.session.commit()

    def __repr__(self):
        return '<World %r (%r)>' % (self.name, self.id)


