import datetime

import jwt
from flask import current_app

from extensions import flask_db as db
from undyingkingdoms.models.bases import GameState


class Token(GameState):
    @staticmethod
    def encode_auth_token():
        """Generate the authentication token.

        :return: string
        """

        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=365),
                'iat': datetime.datetime.utcnow(),
                'sub': current_app.config.get('CLOCK_KEY')
            }
            return jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm=current_app.config.get('JWT_ALGORITHM')
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """Decodes the authentication token.

        :param auth_token
        :return: integer|string
        """

        try:
            payload = jwt.decode(
                auth_token,
                current_app.config.get("SECRET_KEY"),
                algorithms=[current_app.config.get('JWT_ALGORITHM')]
            )
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return "Signature expired. Please log in again."
        except jwt.InvalidTokenError:
            return "Invalid token. Please log in again."


class BlacklistToken(GameState):
    """Token model for storing JWT tokens."""

    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.utcnow()

    @staticmethod
    def check_blacklist(auth_token):
        """Check whether an auth token has been blacklisted."""

        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False

    def __repr__(self):
        return f'<id: token: {self.token}'
