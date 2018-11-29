from random import randint

from flask_login import login_required

from undyingkingdoms import app, db
from undyingkingdoms.models import User, County, Kingdom, World
from undyingkingdoms.static.metadata import kingdom_names


@login_required
@app.route("/reset_schema")
def reset_schema():
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

