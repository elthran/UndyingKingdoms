from flask import url_for, redirect
from undyingkingdoms import app, User, db
from undyingkingdoms.models import Kingdom, County


@app.route('/', methods=['GET', 'POST'])
def home():
    if not User.query.filter().all():
        user = User("elthran", "jacobbrunner@gmail.com", "star")
        db.session.add(user)
        db.session.commit()
        kingdom = Kingdom()
        db.session.add(kingdom)
        db.session.commit()
        county = County("County1", user.id, kingdom.id)
        db.session.add(county)
        db.session.commit()
        user2 = User("elthran2", "jacob.brunner@gmail.com", "star")
        db.session.add(user2)
        db.session.commit()
        county2 = County("County2", user2.id, kingdom.id)
        db.session.add(county2)
        db.session.commit()
    for user in User.query.filter().all():
        print(user.name, user.county.name)
    for kingdom in Kingdom.query.filter().all():
        print(kingdom.name, [(county.name, county.user.name) for county in kingdom.counties])
    return redirect(url_for('login'))
