import os
from datetime import datetime, date
from random import randint

from pandas import DataFrame

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
        self.export_data_to_csv()

    @staticmethod
    def export_data_to_csv():
        all_tables = []
        table_name_reference = []
        tables = db.metadata.tables
        table_names = db.engine.table_names()
        for name in table_names:
            # Each table is a list inside the list
            new_table = []
            table_name_reference.append(name)
            if name not in {}:
                # Each row will be a list inside the table list, inside the all_tables list
                table = tables[name]
                header_row = []
                for column in table.columns:
                    header_row.append(column.name)
                new_table.append(header_row)
                for row in db.session.query(table).all():
                    normal_row = []
                    for value in row:
                        normal_row.append(value)
                    new_table.append(normal_row)
            all_tables.append(new_table)
        # We have a list of smaller lists. Each smaller list should be a csv file (each one is a separate sql table)
        todays_date = date.today()

        current_path = "export/{}".format(todays_date)
        if not os.path.exists(current_path):
            os.makedirs(current_path)

        for index, table in enumerate(all_tables):
            if len(table) < 2:
                continue
            headers = table.pop(0)
            name = table_name_reference[index]

            filename = "{}/{}_table.csv".format(current_path, name)
            df = DataFrame(table)
            df.to_csv(filename, header=headers)

    def __repr__(self):
        return '<World %r (%r)>' % (self.name, self.id)
