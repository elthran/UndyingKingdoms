from undyingkingdoms.models.bases import GameState, db
from undyingkingdoms.models import User


class Chatroom(GameState):

    kingdom_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    content = db.Column(db.String(128))

    def __init__(self, kingdom_id, user_id, content):
        self.kingdom_id = kingdom_id
        self.user_id = user_id
        self.content = content

    def get_county_leader_name(self):
        user = User.query.filter_by(id=self.user_id).first()
        return user.county.leader

    def get_pretty_timestamp(self):
        # This should be improved
        return self.time_created



