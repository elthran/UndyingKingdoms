from .bases import GameState, db


class Notification(GameState):
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.String(128), nullable=False)
    category = db.Column(db.String(32))
    new = db.Column(db.Boolean)
    day = db.Column(db.Integer)  # Which game day it was sent on
    votable = db.Column(db.Boolean)

    county_id = db.Column(db.Integer, db.ForeignKey('county.id'), nullable=False)

    def __init__(self, county, title, content, category="Unknown", votable=False):
        self.county = county
        self.title = title
        self.content = content
        self.category = category
        self.new = True
        self.day = county.kingdom.world.day
        self.votable = votable

    def __repr__(self):
        return '<Notification: %r: %r (%r)>' % (self.title, self.content, self.category)

