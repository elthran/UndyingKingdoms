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
    THREADS_PER_PAGE = 2
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CSRF_ENABLED = True
    CSRF_SESSION_KEY = private_config.CSRF_SESSION_KEY
    JWT_ALGORITHM = 'HS256'
    UPLOAD_FOLDER = 'undyingkingdoms/static/uploads/'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    MAIL_USE_TLS = True
    MAIL_USE_SSL = True
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USERNAME=private_config.MAIL_USERNAME,
    MAIL_PASSWORD=private_config.MAIL_PASSWORD,
    MAIL_DEFAULT_SENDER='This seems to do nothing'


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


class TestingConfig:
    ENV = 'testing'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = MYSQL_BASE.format(
        user=USER, passwd=DB_PASSWORD, host=HOST, dbname=DATABASE_NAME + '_test', options=OPTIONS)
    PRESERVE_CONTEXT_ON_EXCEPTION = False

    # Disable CSRF tokens in the Forms (only valid for testing purposes!)
    WTF_CSRF_ENABLED = False

