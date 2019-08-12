from flask import Blueprint

from flask_wtf.csrf import generate_csrf

from app.api.routes import routes as api_routes
from lib.routing_utils import attach_controller_routes

api_blueprint = Blueprint('api', __name__, url_prefix='/api')

# import all api endpoints
from . import chatroom
from . import forum
from . import infrastructure
from . import military
from . import overview
from . import research

# add in all new style controller routes.
attach_controller_routes(api_blueprint, api_routes)


@api_blueprint.after_request
def set_csrf_header(response):
    response.headers['X-CSRF-Token'] = generate_csrf()
    return response
