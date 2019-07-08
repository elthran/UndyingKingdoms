from flask import url_for

from .base_serializer import Serializer


class ChatroomSerializer(Serializer):
    def __init__(self, message):
        self.time = message.time_created
        self.leader = message.get_county_leader_name()
        self.content = message.content
        self.room = "global" if message.is_global else "kingdom"
        self.id = message.id
        self.leaderURL = url_for('enemy_overview', county_id=message.county_id)
        self.leaderID = message.county_id
