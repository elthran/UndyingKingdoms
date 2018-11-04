from undyingkingdoms.models.bases import GameState, db


class Notification(GameState):

    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.String(128), nullable=False)
    county_id = db.Column(db.Integer, db.ForeignKey('county.id'), nullable=False)

    def __init__(self, county_id, title, content):
        self.county_id = county_id
        self.title = title
        self.content = content

    def __repr__(self):
        return '<Notification: %r: %r>' % (self.title, self.content)

