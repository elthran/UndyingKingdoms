# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from undyingkingdoms import db


class GameState(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class GameEvent(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    server_time = db.Column(db.DateTime, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer)
    activity = db.Column(db.String(16))
    validity = db.Column(db.Boolean)

    def __init__(self, user_id=-1, activity="unknown"):
        self.user_id = user_id
        self.activity = activity
        self.validity = self.validate

    @property
    def validate(self):
        raise NotImplementedError
