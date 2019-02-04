import os
from datetime import datetime, date

from flask import current_app
from pandas import DataFrame

from undyingkingdoms.blueprints import helpers
from undyingkingdoms.models.users import User
from undyingkingdoms.models.dau import DAU
from undyingkingdoms.models.counties import County
from undyingkingdoms.models.kingdoms import Kingdom
from undyingkingdoms.models.bases import GameState

from extensions import flask_db as db


class World(GameState):
    kingdoms = db.relationship('Kingdom', backref='world')
    age = db.Column(db.Integer)  # How many 'reset events'
    day = db.Column(db.Integer)  # How many in-game days have passed this age

    def __init__(self):
        self.age = 1
        self.day = 0

    def advance_day(self):
        for county in County.query.all():
            county.advance_day()
            if county.user.is_bot:
                county.temporary_bot_tweaks()
        self.day += 1

    def advance_24h_analytics(self):
        users = User.query.filter_by(is_bot=False).filter(User.county != None).all()
        for user in users:
            # First check and set their retention
            user_age = (datetime.utcnow() - user.time_created).days
            if user.get_last_login().date() == datetime.today().date():
                retention = 1
            else:
                retention = 0
                user.day1_retention = 1
            if user_age == 1:
                user.day1_retention = retention
            elif user_age == 3:
                user.day3_retention = retention
            elif user_age == 7:
                user.day7_retention = retention
            # If they are playing this age, create a DAU for them
            if user.county:
                dau_event = DAU(user.id, user.county.county_days_in_age, user.county.kingdom.world.day)
                dau_event.save()
        self.export_data_to_csv()

    def advance_age(self):
        users = User.query.all()
        top_user = sorted(users, key=lambda user: user.get_current_leaderboard_score()).pop()

        # the player actually played this round
        if top_user.county is not None:
            top_user.alpha_wins += 1
            top_user.save()

        kingdoms = Kingdom.query.all()
        for kingdom in kingdoms:
            kingdom.leader = 0
            kingdom.save()

        tables = ['county', 'army', 'building', 'notification', 'expedition', 'infiltration', 'chatroom', 'message',
                  'session', 'transaction']
        helpers.drop_then_rebuild_tables(db, tables)
        self.age += 1
        self.day = 0

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
        return '<World %r (%r)>' % ('id:', self.id)
