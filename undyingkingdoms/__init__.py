import os
import socket

from flask import Flask, render_template, send_from_directory
from flask_mail import Mail
from flask_sslify import SSLify

from extensions import flask_db, flask_json, flask_csrf
from undyingkingdoms.GeoIP import geo_ip
from undyingkingdoms.admin import admin_blueprint
from undyingkingdoms.blueprints.game_clock import game_clock_blueprint
import private_config

UPLOAD_FOLDER = 'undyingkingdoms/static/uploads/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config.from_object('config.BaseConfig')
app.config.from_object('private_config')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

sslify = SSLify(app)

if 'liveweb' in socket.gethostname():
    app.config['SQLALCHEMY_DATABASE_URI'] = private_config.SERVER_DATABASE_URI

flask_db.init_app(app)
db = flask_db
flask_csrf.init_app(app)
flask_json.init_app(app)

app.config.update(dict(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME=private_config.MAIL_USERNAME,
    MAIL_PASSWORD=private_config.MAIL_PASSWORD,
    MAIL_DEFAULT_SENDER='This seems to do nothing'
))
mail = Mail(app)

# Register app blueprints
app.register_blueprint(geo_ip)
app.register_blueprint(admin_blueprint)
app.register_blueprint(game_clock_blueprint)


@app.errorhandler(404)
def not_found(error):
    print("Error:", error)
    return render_template('404.html'), 404


from flask_login import LoginManager
from undyingkingdoms.models.users import User


def import_routes():
    import undyingkingdoms.routes.index.home
    import undyingkingdoms.routes.index.login
    import undyingkingdoms.routes.index.register
    import undyingkingdoms.routes.index.logout
    import undyingkingdoms.routes.index.initialize

    import undyingkingdoms.routes.gameplay.overview
    import undyingkingdoms.routes.gameplay.economy
    import undyingkingdoms.routes.gameplay.infrastructure
    import undyingkingdoms.routes.gameplay.military
    import undyingkingdoms.routes.gameplay.infiltration
    import undyingkingdoms.routes.gameplay.kingdom
    import undyingkingdoms.routes.gameplay.attack
    import undyingkingdoms.routes.gameplay.chatroom
    import undyingkingdoms.routes.gameplay.messages

    import undyingkingdoms.routes.gameplay.infiltrate
    import undyingkingdoms.routes.gameplay.temp_upvote

    import undyingkingdoms.routes.user.achievements
    import undyingkingdoms.routes.user.forum
    import undyingkingdoms.routes.user.guide
    import undyingkingdoms.routes.user.leaderboard
    import undyingkingdoms.routes.user.versions
    import undyingkingdoms.routes.hooks


import_routes()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # @login_required will redirect to this page

if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    # Only runs once. If it's a debug relaunch, it won't run
    print("Game ready")


@login_manager.user_loader
def load_user(this_id):
    return User.query.get(this_id)


@app.errorhandler(404)
def not_found(error):
    print("Error:", error)
    return render_template('404.html', error=error), 404


@app.errorhandler(500)
def not_found(error):
    print("Error:", error)
    return render_template('500.html', error=error), 500


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )
