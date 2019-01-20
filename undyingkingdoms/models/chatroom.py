from undyingkingdoms.models.bases import GameState, db
from undyingkingdoms.models import County


class Chatroom(GameState):

    kingdom_id = db.Column(db.Integer)
    county_id = db.Column(db.Integer)
    content = db.Column(db.String(512))

    def __init__(self, kingdom_id, county_id, content):
        self.kingdom_id = kingdom_id
        self.county_id = county_id
        self.content = content

    def get_county_leader_name(self):
        county = County.query.filter_by(id=self.county_id).first()
        return county.leader

    def get_pretty_timestamp(self):
        # This should be improved
        return self.time_created



