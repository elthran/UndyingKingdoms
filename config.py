import private_config

DATABASE_NAME = "undyingkingdoms"

MYSQL_BASE = "mysql+mysqldb://{user}:{passwd}@{host}/{dbname}?{options}"
USER = "elthran"
DB_PASSWORD = private_config.DB_PASSWORD
HOST = "localhost"
OPTIONS = "charset=utf8"


class BaseConfig:
    """Base configuration."""
    ENV = 'base'
    SECRET_KEY = private_config.SECRET_KEY
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CSRF_ENABLED = True
    CSRF_SESSION_KEY = private_config.CSRF_SESSION_KEY


class TestingConfig:
    ENV = 'testing'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = MYSQL_BASE.format(
        user=USER, passwd=DB_PASSWORD, host=HOST, dbname=DATABASE_NAME + '_test', options=OPTIONS)
    PRESERVE_CONTEXT_ON_EXCEPTION = False

    # Disable CSRF tokens in the Forms (only valid for testing purposes!)
    WTF_CSRF_ENABLED = False

