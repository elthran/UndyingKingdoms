from datetime import datetime
from random import randint

from undyingkingdoms.models.users import User
from undyingkingdoms.models import DAU
from undyingkingdoms.models.counties import County
from undyingkingdoms.models.bases import GameState

from extensions import flask_db as db


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
        while (self.day // 24) > self.analytic_cycles:  # First advance DAU since it runs a day behind and should get the older data.
            self.advance_24h_analytics()
            self.analytic_cycles += 1
        while now != self.game_clock:  # Now advance all the game clocks and events.
            self.advance_day()
            self.game_clock = (self.game_clock + 1) % 24
        if self.day >= 2:
            self.advance_age()

    def advance_day(self):
        for county in County.query.all():
            county.advance_day()
        self.day += 1

    def advance_age(self):
        """Refresh the play experience.

        +1 to the current age, set the day to 0,
        reset game data, not including user nor metadata.
        """
        self.age += 1
        self.day = 0

    def advance_24h_analytics(self):
        users = User.query.all()
        for user in users:
            # Create a DAU row
            dau_event = DAU(user.id, self.day)
            # Update User analytics
            user_age = (datetime.now() - user.time_created).days
            if user_age == 1:
                user.day1_retention = randint(0, 1)
            elif user_age == 3:
                user.day3_retention = randint(0, 1)
            elif user_age == 7:
                user.day7_retention = randint(0, 1)
            dau_event.save()


    def __repr__(self):
        return '<World %r (%r)>' % (self.name, self.id)