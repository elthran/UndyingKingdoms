from datetime import datetime, timedelta

from undyingkingdoms import db
from undyingkingdoms.models import Session, User
from undyingkingdoms.models.bases import GameEvent


class DAU(GameEvent):
	# User data
	user_id = db.Column(db.Integer)
	account_age_in_days = db.Column(db.Integer)
	sessions = db.Column(db.Integer)
	minutes_played = db.Column(db.Integer)
	ads_watched = db.Column(db.Integer)
	# Game data
	days_in_age = db.Column(db.Integer)
	land = db.Column(db.Integer)
	population = db.Column(db.Integer)
	gold = db.Column(db.Integer)
	happiness = db.Column(db.Integer)
	hunger = db.Column(db.Integer)

	def __init__(self, user_id, day):
		self.user_id = user_id
		self.days_in_age = day
		self.sessions = self.get_sessions(user_id)
		self.minutes_played = self.get_minutes_played(user_id)
		self.ads_watched = 0
		self.update_self(user_id)

	def update_self(self, user_id):
		user = User.query.filter_by(id=user_id).first()
		county = user.county
		self.account_age_in_days = (datetime.now() - user.time_created).days
		self.land = county.land
		self.population = county.population
		self.gold = county.gold
		self.happiness = county.happiness
		self.hunger = county.hunger

	@staticmethod
	def get_sessions(user_id):
		yesterday = datetime.now().date() - timedelta(days=1)
		return Session.query.filter_by(user_id=user_id, activity="login", date_created=yesterday).count()

	@staticmethod
	def get_minutes_played(user_id):
		yesterday = datetime.now().date() - timedelta(days=1)
		sessions = Session.query.filter_by(user_id=user_id, activity="logout", date_created=yesterday).all()
		return sum(session.minutes for session in sessions)
