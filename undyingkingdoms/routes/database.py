from datetime import date

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
    # Create a list of all tables
    all_tables = []
    table_name_reference = []
    tables = db.metadata.tables
    table_names = db.engine.table_names()
    for name in table_names:
        # Each table is a list inside the list
        new_table = []
        table_name_reference.append(name)
        if name not in {'authentication_event', 'daily_active_user'}:
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
    for index, table in enumerate(all_tables):
        if len(table) < 2:
            continue
        headers = table.pop(0)
        name = table_name_reference[index]
        filename = "{}-{}_table.csv".format(todays_date, name)
        df = DataFrame(table)
        df.to_csv(filename, header=headers)
    return "Database exported successfully"


