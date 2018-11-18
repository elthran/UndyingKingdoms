import flask

from undyingkingdoms import app, db


@app.route("/reset_schema")
def reset_schema():
    from flask_login import current_user
    if current_user.name not in ['...']:
        pass
        # redirect away from page
    db.drop_all()
    db.create_all()
    return "Rebuilt database schema"
