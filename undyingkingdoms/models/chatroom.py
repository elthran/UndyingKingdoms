from undyingkingdoms.models.bases import GameState, db
from undyingkingdoms.models import County


class Chatroom(GameState):

    kingdom_id = db.Column(db.Integer)
    county_id = db.Column(db.Integer)
    content = db.Column(db.String(512))
    is_global = db.Column(db.Boolean, default=False)

    def __init__(self, kingdom_id, county_id, content, is_global=False):
        self.kingdom_id = kingdom_id
        self.county_id = county_id
        self.content = content
        self.is_global = is_global

    def get_county_leader_name(self):
        county = County.query.filter_by(id=self.county_id).first()
        return county.leader

    def get_pretty_timestamp(self):
        # This should be improved
        return str(self.time_created)[11:19]

    def json_ready(self):
        # return "({time}) {leader}: {content}".format(time=self.get_pretty_timestamp(), leader=self.get_county_leader_name(), content=self.content)
        return self.time_created, self.get_county_leader_name(), self.content
