# Magical built-in function relating to sockets?
import socket

# Import flask and template operators
from flask import Flask, render_template

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# CSRF Protection
from flask_wtf.csrf import CSRFProtect

# Import JSON
from flask_json import FlaskJSON

# Import mailing
from flask_mail import Mail

# Imports settings from the private security file
import private_config

UPLOAD_FOLDER = 'undyingkingdoms/static/uploads/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Define the WSGI application object
app = Flask(__name__)

# Configurations (Klondikemarlen suggest moving the configs to the config file. Smart idea! Will implement)
app.config.from_object('private_config')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Check location of code whether server or local
if 'liveweb' in socket.gethostname():  # Running on server (pythonanywhere)
    app.config['SQLALCHEMY_DATABASE_URI'] = private_config.SERVER_DATABASE_URI

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Ensbles CSRF protection
csrf = CSRFProtect(app)
csrf.init_app(app)

# Enables JSON
json = FlaskJSON(app)

# Enables mailing
app.config.update(dict(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME=private_config.MAIL_USERNAME,
    MAIL_PASSWORD=private_config.MAIL_PASSWORD,
    MAIL_DEFAULT_SENDER='This seems to do nothing'
))
mail = Mail(app)


# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    print("Error:", error)
    return render_template('404.html'), 404


# This will handle user requests. Needs to be imported after the database is set up
from flask_login import LoginManager
from undyingkingdoms.models.users import User

import undyingkingdoms.routes.index.home
import undyingkingdoms.routes.index.login
import undyingkingdoms.routes.index.logout

import undyingkingdoms.routes.gameplay.overview
import undyingkingdoms.routes.gameplay.economy
import undyingkingdoms.routes.gameplay.infrastructure
import undyingkingdoms.routes.gameplay.military
import undyingkingdoms.routes.gameplay.kingdom


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Build the tables in database, if the database exists.
# Otherwise build using mysql: CREATE DATABASE IF NOT EXISTS booking CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

db.drop_all()
db.create_all()


@login_manager.user_loader
def load_user(this_id):
    return User.query.get(this_id)
