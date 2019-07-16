import os
import socket

from flask import Flask, send_from_directory
from flask_sslify import SSLify
from flask_login import LoginManager

from extensions import (
    flask_db, flask_csrf, flask_mobility, flask_mail, flask_cors,
    flask_serializer
)
from app.GeoIP import geo_ip
from app.blueprints.admin import admin_blueprint
from app.blueprints.game_clock import game_clock_blueprint
from app.api import api_blueprint

app = Flask(__name__)
# I can't figure out how to put these in the config file
app.jinja_env.lstrip_blocks = True
app.jinja_env.trim_blocks = True
app.config.from_object('private_config')

# TODO: come up with better test for production mode.
if 'live' in socket.gethostname():
    app.config.from_object('config.ProductionConfig')
else:
    app.config.from_object('config.DevelopmentConfig')
from app import jinja_addons

sslify = SSLify(app)
flask_db.init_app(app)
db = flask_db
flask_csrf.init_app(app)
flask_mobility.init_app(app)
flask_mail.init_app(app)
flask_serializer.init_app(app)

if app.config['ENV'] != 'production':
    flask_cors.init_app(app)

# Register app blueprints
app.register_blueprint(geo_ip)
app.register_blueprint(admin_blueprint)
app.register_blueprint(game_clock_blueprint)
app.register_blueprint(api_blueprint)

from app.models.exports import User


def import_routes():
    import app.routes.errors
    import app.routes.index.home
    import app.routes.index.login
    import app.routes.index.register
    import app.routes.index.logout
    import app.routes.index.initialize
    import app.routes.index.activate

    import app.routes.gameplay.overview
    import app.routes.gameplay.economy
    import app.routes.gameplay.merchant
    import app.routes.gameplay.infrastructure
    import app.routes.gameplay.military
    import app.routes.gameplay.infiltration
    import app.routes.gameplay.casting
    import app.routes.gameplay.research
    import app.routes.gameplay.trading
    import app.routes.gameplay.kingdom
    import app.routes.gameplay.attack
    import app.routes.gameplay.messages
    import app.routes.gameplay.royal_court
    import app.routes.clans.generic_clan
    import app.routes.gameplay.chatroom
    import app.routes.gameplay.infiltrate

    import app.routes.user.achievements
    import app.routes.user.forum
    import app.routes.user.profile
    import app.routes.user.guide
    import app.routes.user.leaderboard
    import app.routes.hooks


import_routes()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # @login_required will redirect to this page
# returns unauthorized (401) if fails @login_required for 'api' route.
login_manager.blueprint_login_views[api_blueprint.name] = None

if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    # Only runs once. If it's a debug relaunch, it won't run
    print("Game ready")


@login_manager.user_loader
def load_user(this_id):
    return User.query.get(this_id)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )
