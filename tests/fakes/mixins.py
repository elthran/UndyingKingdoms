from extensions import flask_db


class SQLAlcMeta:
    sqlalchemy_session = flask_db.session
    sqlalchemy_session_persistence = 'commit'
