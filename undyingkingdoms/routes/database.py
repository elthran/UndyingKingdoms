import csv
from datetime import datetime

from flask import render_template
from flask_login import login_required

from undyingkingdoms import app, db
from undyingkingdoms.models import User, County, Kingdom, World
from undyingkingdoms.static.metadata import kingdom_names


@login_required
@app.route("/database/<string:command>/")
def database(command=""):
    if command == "reset":
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
        return "Rebuilt database schema!"
    if command == "export":
        # filename = str(datetime.now()) + ".csv"
        # outfile = open(filename, 'wb')
        # outcsv = csv.writer(outfile)
        all_users = User.query.all()
        database_csv = []
        new_row = []
        for column in User.__table__.columns:
            new_row.append(str(column))
        database_csv.append(new_row)
        for user in all_users:
            new_row = []
            for column in User.__table__.columns:
                column_name = str(column)[5:]
                new_row.append(str(getattr(user, column_name)))
            database_csv.append(new_row)
        return render_template('temporary_database.html', database_csv=database_csv)
        # [outcsv.writerow([getattr(user, column.name) for column in User.__mapper__.column_attrs.keys()]) for user in all_users]
        # outfile.close()
        # return "exported database"


