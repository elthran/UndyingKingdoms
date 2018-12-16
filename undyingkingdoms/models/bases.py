from undyingkingdoms import db


class GameState(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    time_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    time_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class GameEvent(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    time_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer)

