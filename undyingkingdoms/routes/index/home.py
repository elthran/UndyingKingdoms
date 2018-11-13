import datetime

from flask import url_for, redirect
from undyingkingdoms import app, db
from undyingkingdoms.models import User, County, Kingdom


@app.route('/', methods=['GET', 'POST'])
def home():
    if not User.query.filter().all():
        print("BUILDING EVERYTHING")
        user = User("elthran", "jacobbrunner@gmail.com", "star")
        db.session.add(user)
        db.session.commit()
        kingdom = Kingdom()
        db.session.add(kingdom)
        db.session.commit()
        county = County("County1", "John", user.id, kingdom.id, 'Dwarf', 'Male')
        db.session.add(county)
        db.session.commit()
        user2 = User("timekeeper", "xxx", "xxx")
        db.session.add(user2)
        db.session.commit()
        county2 = County("Time Warp", "The Timekeeper", user2.id, kingdom.id, 'Human', 'Female')
        county2.total_land = datetime.datetime.now().hour
        db.session.add(county2)
        db.session.commit()
    else:
        print("EVERYTHING IS ALREADY BUILT")
    return redirect(url_for('login'))
