from undyingkingdoms.models.bases import GameState, db


class Upvote(GameState):

    user_id = db.Column(db.Integer)
    post_id = db.Column(db.Integer)
    vote = db.Column(db.Integer)

    def __init__(self, user_id, post_id, vote):
        self.user_id = user_id
        self.post_id = post_id
        self.vote = vote

    def __repr__(self):
        return '<Notification: %r: %r>' % (self.title, self.content)

