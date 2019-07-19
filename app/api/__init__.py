from flask import Blueprint

from extensions import flask_csrf

from app.api.routes import routes as api_routes
from lib.routing_utils import attach_controller_routes

api_blueprint = Blueprint('api', __name__, url_prefix='/api')
# TODO: remove this in production?
flask_csrf.exempt(api_blueprint)

# import all api endpoints
from . import chatroom
from . import forum
from . import infrastructure
from . import military
from . import overview
from . import research

# add in all new style controller routes.
attach_controller_routes(api_blueprint, api_routes)
