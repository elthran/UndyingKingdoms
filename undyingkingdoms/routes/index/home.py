from flask import url_for, redirect
from undyingkingdoms import app, db
from undyingkingdoms.models import User, County, Kingdom, World


@app.route('/', methods=['GET', 'POST'])
def home():
    if not User.query.filter().all():
        world = World()
        db.session.add(world)
        db.session.commit()
        print("BUILDING EVERYTHING")
        user = User("elthran", "jacobbrunner@gmail.com", "star")
        db.session.add(user)
        db.session.commit()
        kingdom = Kingdom()
        db.session.add(kingdom)
        db.session.commit()
        county = County("Elthrania", "Elthran", user.id, kingdom.id, 'Dwarf', 'Male')
        db.session.add(county)
        db.session.commit()
        county.vote = county.id
        db.session.commit()
    else:
        print("EVERYTHING IS ALREADY BUILT")
    return redirect(url_for('login'))
