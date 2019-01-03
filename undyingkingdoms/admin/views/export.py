import os
from datetime import date

from flask import jsonify
from flask.views import MethodView
from flask_login import login_required
from pandas import DataFrame

from extensions import flask_db as db


class ExportAPI(MethodView):
    @login_required
    def get(self):
        # Todo: consider making data write out line by line.
        # This will become very important once the data size is large.

        # Create a list of all tables
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
        return jsonify(
            status='success',
            message="Database exported successfully"
        ), 200
