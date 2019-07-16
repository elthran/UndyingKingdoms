from flask import url_for

# if installed: from flask_serializer import Serializer
from lib.flask_serializer.flask_serializer import Serializer


class ChatroomSerializer(Serializer):
    def __init__(self, obj):
        self.time = obj.time_created
        self.leader = obj.get_county_leader_name()
        self.content = obj.content
        self.room = "global" if obj.is_global else "kingdom"
        self.id = obj.id
        self.leaderURL = url_for('enemy_overview', county_id=obj.county_id)
        self.leaderID = obj.county_id


