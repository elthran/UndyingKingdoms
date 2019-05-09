import os
import socket

from flask import Flask, send_from_directory
from flask_sslify import SSLify
from flask_login import LoginManager

from extensions import flask_db, flask_json, flask_csrf, flask_mobility, flask_mail, flask_cors
from undyingkingdoms.GeoIP import geo_ip
from undyingkingdoms.blueprints.admin import admin_blueprint
from undyingkingdoms.blueprints.game_clock import game_clock_blueprint
from undyingkingdoms.api import api_blueprint

app = Flask(__name__)
# I can't figure out how to put these in the config file
app.jinja_env.lstrip_blocks = True
app.jinja_env.trim_blocks = True
app.config.from_object('private_config')

if 'live' in socket.gethostname():
    app.config.from_object('config.ProductionConfig')
else:
    app.config.from_object('config.DevelopmentConfig')
from undyingkingdoms import jinja_addons

sslify = SSLify(app)
flask_db.init_app(app)
db = flask_db
flask_csrf.init_app(app)
flask_json.init_app(app)
flask_mobility.init_app(app)
flask_mail.init_app(app)

if app.config['ENV'] != 'production':
    flask_cors.init_app(app)

# Register app blueprints
app.register_blueprint(geo_ip)
app.register_blueprint(admin_blueprint)
app.register_blueprint(game_clock_blueprint)
app.register_blueprint(api_blueprint)

from undyingkingdoms.models.exports import User


def import_routes():
    import undyingkingdoms.routes.errors
    import undyingkingdoms.routes.index.home
    import undyingkingdoms.routes.index.login
    import undyingkingdoms.routes.index.register
    import undyingkingdoms.routes.index.logout
    import undyingkingdoms.routes.index.initialize
    import undyingkingdoms.routes.index.activate

    import undyingkingdoms.routes.gameplay.overview
    import undyingkingdoms.routes.gameplay.economy
    import undyingkingdoms.routes.gameplay.infrastructure
    import undyingkingdoms.routes.gameplay.military
    import undyingkingdoms.routes.gameplay.infiltration
    import undyingkingdoms.routes.gameplay.casting
    import undyingkingdoms.routes.gameplay.research
    import undyingkingdoms.routes.gameplay.trading
    import undyingkingdoms.routes.gameplay.kingdom
    import undyingkingdoms.routes.gameplay.attack
    import undyingkingdoms.routes.gameplay.messages
    import undyingkingdoms.routes.gameplay.royal_court
    import undyingkingdoms.routes.clans.generic_clan
    import undyingkingdoms.routes.gameplay.chatroom
    import undyingkingdoms.routes.gameplay.infiltrate

    import undyingkingdoms.routes.user.achievements
    import undyingkingdoms.routes.user.forum
    import undyingkingdoms.routes.user.profile
    import undyingkingdoms.routes.user.guide
    import undyingkingdoms.routes.user.leaderboard
    import undyingkingdoms.routes.hooks


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
