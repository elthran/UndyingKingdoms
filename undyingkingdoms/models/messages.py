from flask import url_for

from .bases import GameState, db
from .exports import County, World


class Message(GameState):

    county_id = db.Column(db.Integer, db.ForeignKey('county.id'), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.String(5000), nullable=False)
    author_county_id = db.Column(db.Integer)
    unread = db.Column(db.Boolean)
    day = db.Column(db.Integer)  # Which game day it was sent on

    def __init__(self, county_id, title, content, author_county_id, day):
        self.county_id = county_id
        self.title = title
        self.content = content
        self.author_county_id = author_county_id
        self.unread = True
        self.day = day

    def __repr__(self):
        return '<Notification: %r: %r>' % (self.title, self.content)

    def get_author(self):
        county = County.query.get(self.author_county_id)
        return county.leader

    def get_reply_url(self):
        county = County.query.get(self.author_county_id)
        return url_for('enemy_overview', county_id=county.id)

    def get_age_of_message(self):
        current_day = World.query.get(1).day
        return current_day - self.day


