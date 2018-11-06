from undyingkingdoms.models.bases import GameState, db
from werkzeug.security import generate_password_hash, check_password_hash
from undyingkingdoms.models.counties import County


class User(GameState):

    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password_hash = db.Column(db.String(192), nullable=False)
    phone = db.Column(db.Integer)
    county = db.relationship('County', backref='user', uselist=False)

    is_authenticated = db.Column(db.Boolean)
    is_active = db.Column(db.Boolean)
    is_anonymous = db.Column(db.Boolean)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.set_password_hash(password)
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False

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

