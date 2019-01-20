from undyingkingdoms.models.bases import GameState, db


class Notification(GameState):

    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.String(128), nullable=False)
    county_id = db.Column(db.Integer, db.ForeignKey('county.id'), nullable=False)
    new = db.Column(db.Boolean)
    day = db.Column(db.Integer)  # Which game day it was sent on

    def __init__(self, county_id, title, content, day):
        self.county_id = county_id
        self.title = title
        self.content = content
        self.new = True
        self.day = day

    def __repr__(self):
        return '<Notification: %r: %r>' % (self.title, self.content)

