from flask_sqlalchemy import SQLAlchemy
from flask_json import FlaskJSON
from flask_wtf.csrf import CSRFProtect
# from flask_sslify import SSLify  # currently doesn't support factory pattern
from flask_mobility import Mobility
from flask_mail import Mail
from flask_cors import CORS

# Initialize database
flask_db = SQLAlchemy()
flask_json = FlaskJSON()
flask_csrf = CSRFProtect()
# flask_sslify = SSLify()
flask_mobility = Mobility()
flask_mail = Mail()
# cors config (
# CORS(resources={
#     r"/api/*": {"origins": "*"},
#     r"/login/": {"origins": "*"}
# }
flask_cors = CORS(supports_credentials=True)
