import flask

from extensions import flask_db as db
from undyingkingdoms.models.bases import GameEvent


class Session(GameEvent):
    time_logged_out = db.Column(db.DateTime)
    user_id = db.Column(db.Integer)
    county_day = db.Column(db.Integer)
    minutes = db.Column(db.Integer)
    cookie_id = db.Column(db.String(128))

    def __init__(self, user_id, county_day):
        self.user_id = user_id
        self.county_day = county_day
        self.seconds = None
        self.valid = True

    def set_minutes(self):
        if self.time_created is None or self.time_logged_out == self.time_created:
            self.minutes = 0
        else:
            self.minutes = (self.time_logged_out - self.time_created).seconds // 60
    @staticmethod
    def get_last_by_time(id):
        return Session.query.filter_by(user_id=id).order_by(db.desc('time_created')).first()

    @staticmethod
    def get_anon_session():
        return Session.query.filter_by(cookie_id=flask.session['_id']).one_or_none()

    @staticmethod
    def anon_session():
        anon_session = Session.get_anon_session()
        if anon_session is None:
            anon_session = Session(None, None)
            anon_session.cookie_id = flask.session['_id']
            anon_session.save()

        return anon_session
