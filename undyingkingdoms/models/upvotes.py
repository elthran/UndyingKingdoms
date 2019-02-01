from undyingkingdoms.models.bases import GameState, db


class Upvote(GameState):

    user_id = db.Column(db.Integer)
    post_id = db.Column(db.Integer)
    vote = db.Column(db.Integer)

    def __init__(self, user_id, post_id, vote):
        self.user_id = user_id
        self.post_id = post_id
        self.vote = vote

    def toggle_vote(self):
        """toggles vote on or off, depending on current state.

        if vote is 1, sets vote to 0, if vote is 0 sets it to 1.
        """

        self.vote = 1 - self.vote

    def __repr__(self):
        return '<Notification: %r: %r>' % (self.title, self.content)

