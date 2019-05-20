import private_config

SITE_URL = 'https://www.undyingkingdoms.com'
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
    THREADS_PER_PAGE = 2
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # I don't know what these do but we might need them at some point.
    # from server show global variables like '%connections%';
    SQLALCHEMY_POOL_SIZE = 5000
    SQLALCHEMY_POOL_RECYCLE = 30 * 60  # 30 minutes, sounded reasonable?
    # sounded reasonable, maybe should be same as SQLALCHEMY_POOL_RECYCLE
    SQLALCHEMY_POOL_TIMEOUT = 30

    CSRF_ENABLED = True
    CSRF_SESSION_KEY = private_config.CSRF_SESSION_KEY
    JWT_ALGORITHM = 'HS256'
    UPLOAD_FOLDER = 'undyingkingdoms/static/uploads/'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

class ProductionConfig(BaseConfig):
    ENV = 'production'
    DEBUG = False
    SQLALCHEMY_POOL_RECYCLE = 299  # 1s less than PythonAnywhere's 300s (5 min).
    SQLALCHEMY_DATABASE_URI = private_config.SERVER_DATABASE_URI


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    ENV = 'development'
    DEBUG = True
    if DEBUG:
        SSLIFY_DISABLE = True
    SQLALCHEMY_DATABASE_URI = MYSQL_BASE.format(
        user=USER, passwd=DB_PASSWORD, host=HOST, dbname=DATABASE_NAME, options=OPTIONS)


class TestingConfig:
    ENV = 'testing'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = MYSQL_BASE.format(
        user=USER, passwd=DB_PASSWORD, host=HOST, dbname=DATABASE_NAME + '_test', options=OPTIONS)
    PRESERVE_CONTEXT_ON_EXCEPTION = False

    # Disable CSRF tokens in the Forms (only valid for testing purposes!)
    WTF_CSRF_ENABLED = False

    # show all sql queries
    # SQLALCHEMY_ECHO = True

