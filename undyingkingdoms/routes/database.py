from datetime import date
import os

from flask_login import login_required
from pandas import DataFrame

from undyingkingdoms import app, db
from undyingkingdoms.models import User, County, Kingdom, World
from undyingkingdoms.static.metadata import kingdom_names


@login_required
@app.route("/database/reset/")
def database_reset():
    # Should make it so only admin can visit
    db.drop_all()
    db.create_all()
    # Create the game world
    world = World()
    db.session.add(world)
    db.session.commit()
    # Create all the kingdoms
    for i in range(len(kingdom_names)):
        kingdom = Kingdom(kingdom_names[i])
        db.session.add(kingdom)
        db.session.commit()
    # Create AI
    user = User("ai", "ai@gmail.com", "star")
    user.is_admin = True
    user.is_active = True
    db.session.add(user)
    db.session.commit()
    # Create AI's county
    county = County("Robotica", "Mr. Roboto", user.id, 'Human', 'Demale')
    db.session.add(county)
    db.session.commit()
    county.vote = county.id
    county.armies['peasant'].amount = 0
    db.session.commit()
    # Create Elthran
    user = User("elthran", "jacobbrunner@gmail.com", "star")
    user.is_admin = True
    user.is_active = True
    db.session.add(user)
    db.session.commit()
    # Create Elthran's county
    county = County("Ulthuan", "Elthran", user.id, 'Dwarf', 'Male')
    db.session.add(county)
    db.session.commit()
    county.vote = county.id
    db.session.commit()
    return "Database has been deleted and rebuilt."


@login_required
@app.route("/database/export/")
def database_export():
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
        if name not in {'authentication_event', 'dau'}:
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
    return "Database exported successfully"


