from flask import url_for

from .base_serializer import Serializer


class ChatroomSerializer(Serializer):
    def __init__(self, chat_message):
        self.time = chat_message.time_created
        self.leader = chat_message.get_county_leader_name()
        self.content = chat_message.content
        self.room = "global" if chat_message.is_global else "kingdom"
        self.id = chat_message.id
        self.leaderURL = url_for('enemy_overview', county_id=chat_message.county_id)
        self.leaderID = chat_message.county_id


