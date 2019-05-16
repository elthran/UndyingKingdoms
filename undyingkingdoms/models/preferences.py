from datetime import datetime, timedelta
from random import choice

from sqlalchemy import desc

from undyingkingdoms.models.exports import Chatroom, Message
from .bases import GameState, db


class Preferences(GameState):
    BASE_TAX_RATE = 8

    county_id = db.Column(db.Integer, db.ForeignKey('county.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship("User", back_populates='preferences')

    global_chat_on = db.Column(db.Boolean, default=False)
    _tax_rate = db.Column(db.Integer)
    rations = db.Column(db.Float)
    production_choice = db.Column(db.Integer)
    research_choice_id = db.Column(db.Integer, db.ForeignKey('technology.id'))
    research_choice = db.relationship("Technology")
    vote_id = db.Column(db.Integer, db.ForeignKey('county.id'))
    last_vote_date = db.Column(db.DateTime)
    weather = db.Column(db.String(32))
    days_since_event = db.Column(db.Integer)
    produce_land = db.Column(db.Integer)  # Progress towards next land

    last_checked_townhall = db.Column(db.DateTime, default=datetime.utcnow)

    weather_choices = ["clear skies", "stormy", "sunny", "cloudy", "light rain", "overcast"]

    @property
    def tax_rate(self):
        return self._tax_rate or 0

    @tax_rate.setter
    def tax_rate(self, value):
        """Set tax rate.

        Tax rate has a flat reduction to happiness change.
        """
        county = self.county
        county.happiness_change -= (value - self.tax_rate)
        self._tax_rate = value

    def all_messages_query(self):
        return Chatroom.query.filter(Chatroom.is_global | (Chatroom.kingdom_id == self.county.kingdom_id))

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

    def __init__(self, county, user):
        self.county = county
        self.user = user
        self.tax_rate = self.BASE_TAX_RATE
        self.rations = 1
        self.production_choice = county.GOLD
        self.research_choice = choice(list(county.available_techs))
        self.vote = county
        self.last_vote_date = None
        self.weather = "Sunny"
        self.days_since_event = 0
        self.produce_land = 0  # Progress towards next land

    def get_votes_for_self(self):
        """
        Checks how many counties have voted for you to be king
        """
        return Preferences.query.filter_by(vote_id=self.county_id).count()
