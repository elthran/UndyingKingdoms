from datetime import datetime, timedelta

from sqlalchemy import desc

from undyingkingdoms.models import Chatroom, Message
from undyingkingdoms.models.bases import GameState, db


class Preferences(GameState):

    county_id = db.Column(db.Integer, db.ForeignKey('county.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    global_chat_on = db.Column(db.Boolean, default=False)
    tax_rate = db.Column(db.Integer)
    rations = db.Column(db.Float)
    production_choice = db.Column(db.Integer)
    research_choice = db.Column(db.String(128))
    vote = db.Column(db.Integer)
    last_vote_date = db.Column(db.DateTime)
    weather = db.Column(db.String(32))
    days_since_event = db.Column(db.Integer)
    produce_land = db.Column(db.Integer)  # Progress towards next land

    last_checked_townhall = db.Column(db.DateTime, default=datetime.utcnow)

    weather_choices = ["clear skies", "stormy", "sunny", "cloudy", "light rain", "overcast"]

    def all_messages_query(self):
        return Chatroom.query.filter((Chatroom.is_global) | (Chatroom.kingdom_id == self.county.kingdom_id))

    def has_mail(self):
        return Message.query.filter_by(county_id=self.county_id, unread=True).first() is not None

    def has_new_townhall_message(self):
        last_chat_time = self.last_chat_time
        if last_chat_time and ((self.last_checked_townhall + timedelta(seconds=2)) < last_chat_time):
            return True
        return False

    @property
    def last_chat_time(self):
        most_recent_message = self.all_messages_query().order_by(desc('time_created')).first()
        if most_recent_message is not None:
            self.global_chat_on = most_recent_message.is_global
            return most_recent_message.time_created

    def __init__(self, county_id, user_id):
        self.county_id = county_id
        self.user_id = user_id
        self.tax_rate = 8
        self.rations = 1
        self.production_choice = 0
        self.research_choice = 'agriculture'
        self.vote = county_id
        self.last_vote_date = None
        self.weather = "Sunny"
        self.days_since_event = 0
        self.produce_land = 0  # Progress towards next land

    def get_votes_for_self(self):
        """
        Checks how many counties have voted for you to be king
        """
        return Preferences.query.filter_by(vote=self.county_id).count()
