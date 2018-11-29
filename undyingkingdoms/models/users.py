from undyingkingdoms.models.bases import GameState, db
from werkzeug.security import generate_password_hash, check_password_hash
from undyingkingdoms.models.counties import County


class User(GameState):
    # Basic data
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password_hash = db.Column(db.String(192), nullable=False)
    phone_number = db.Column(db.Integer)
    county = db.relationship('County', backref='user', uselist=False)
    achievements = db.relationship('Achievement', backref='user')

    # Analytics
    ages_completed = db.Column(db.Integer)
    day1_retention = db.Column(db.Integer)
    day3_retention = db.Column(db.Integer)
    day7_retention = db.Column(db.Integer)
    lifetime_revenue = db.Column(db.Integer)
    country = db.Column(db.String(32))
    ip_address = db.Column(db.String(32))

    # Flask
    is_authenticated = db.Column(db.Boolean)  # User has logged in
    is_active = db.Column(db.Boolean)  # Account has been activated via email and not been locked
    is_anonymous = db.Column(db.Boolean)  # current_user is set to is_anonymous when not yet logged in.
    is_admin = db.Column(db.Boolean)  # Current user is a game creator with unlimited power

    def __init__(self, username, email, password):
        # Basic data
        self.username = username
        self.email = email
        self.set_password_hash(password)

        # Analytics
        self.ages_completed = 0
        self.day1_retention = None
        self.day3_retention = None
        self.day7_retention = None
        self.lifetime_revenue = 0
        self.country = ""
        self.ip_address = ""

        # Flask login
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False
        self.is_admin = False

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute. Only password_hash is stored.')

    def set_password_hash(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.id

    def has_county(self):
        return True if County.query.filter_by(user_id=self.id) else False

    def __repr__(self):
        return '<User %r (%r)>' % (self.name, self.id)

