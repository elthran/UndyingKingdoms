import os
from datetime import datetime

from pandas import DataFrame

from undyingkingdoms.utilities import table_mixers
from .exports import User
from .exports import DAU
from .exports import County
from .exports import Kingdom
from .bases import GameState

from extensions import flask_db as db

seasons = ["Spring", "Summer", "Autumn", "Winter"]


class World(GameState):
    kingdoms = db.relationship('Kingdom', backref='world')
    age = db.Column(db.Integer)  # How many 'reset events'
    day = db.Column(db.Integer)  # How many in-game days have passed this age
    season = db.Column(db.String(16))  # The current season

    def __init__(self):
        self.age = 1
        self.day = 0
        self.season = seasons[0]

    def advance_day(self):
        if self.day >= 0:
            for county in County.query.all():
                if county.user.is_bot:
                    county.temporary_bot_tweaks()
                else:
                    county.advance_day()
            for kingdom in Kingdom.query.all():
                kingdom.advance_day()

        self.day += 1
        if self.day % 36 == 0:  # Every 36 game days we advance the game season
            season_index = seasons.index(self.season) + 1
            if season_index == len(seasons):
                season_index = 0
            self.season = seasons[season_index]
            
    def advance_analytics(self):
        if self.day < 0:
            return
        users = User.query.filter_by(is_bot=False).filter(User.county != None).all()
        for user in users:
            # First check and set their retention
            user_age = (datetime.utcnow() - user.time_created).days
            if user.get_last_logout() and user.get_last_logout().date() == datetime.today().date():
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
                dau_event = DAU(user.id)
                dau_event.save()
        self.export_data_to_csv()

    def advance_age(self):
        kingdoms = Kingdom.query.all()
        counties = County.query.all()
        users = User.query.all()
        for user in users:
            if user.county:
                user.ages_completed += 1
        for kingdom in kingdoms:
            kingdom.leader = 0
            kingdom.wars_total_ta = 0
            kingdom.wars_won_ta = 0
            kingdom.approval_rating = None
            kingdom.save()
        winning_kingdoms = [sorted(kingdoms, key=lambda x: x.wars_won_ta, reverse=True)[0],
                            sorted(kingdoms, key=lambda x: x.total_land_of_top_three_counties, reverse=True)[0]]
        winning_county = sorted(counties, key=lambda x: x.land, reverse=True)[0]
        for kingdom in winning_kingdoms:
            for county in kingdom.counties:
                county.user.gems += 1
        winning_county.user.gems += 1

        tables = ['DAU', 'army', 'building', 'casting', 'chatroom', 'diplomacy', 'economy', 'espionage', 'expedition',
                  'infiltration', 'infrastructure', 'magic', 'message', 'military', 'notification', 'preferences',
                  'scientist', 'session', 'tech_to_tech', 'technology', 'trade', 'transaction', 'wizardry',
                  'county']
        table_mixers.drop_then_rebuild_tables(db, tables)
        self.age += 1
        self.day = -12

    def export_data_to_csv(self):
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
        current_path = f"export/age-{self.age}"
        if not os.path.exists(current_path):
            os.makedirs(current_path)

        for index, table in enumerate(all_tables):
            if len(table) < 2:
                continue
            headers = table.pop(0)
            name = table_name_reference[index]

            filename = f"{current_path}/{name}_table.csv"
            df = DataFrame(table)
            df.to_csv(filename, header=headers)

    def __repr__(self):
        return '<World %r (%r)>' % ('id:', self.id)
