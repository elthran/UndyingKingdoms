from importlib import import_module

from flask import Blueprint

from extensions import flask_csrf
from lib.namers import to_class_name

from app.api.routes import routes as api_routes
from lib.routing_utils import attach_controller_routes

api_blueprint = Blueprint('api', __name__, url_prefix='/api')
# TODO: remove this in production?
flask_csrf.exempt(api_blueprint)

# import all api endpoints
from . import chatroom
from . import forum
from . import overview
from . import research
from . import military

endpoints = {
    'sidebar': None,
}

for endpoint in endpoints:
    mod = import_module('.' + endpoint, __name__)
    class_name = to_class_name(endpoint) + 'API'
    Class = getattr(mod, class_name)
    try:  # add optional path arguments
        path = endpoints[endpoint]['path_args']
    except (KeyError, TypeError):
        path = ''
    api_blueprint.add_url_rule(
        f'/{endpoint}{path}',
        view_func=Class.as_view(f'{endpoint}_api')
    )


# add in all new style controller routes.
attach_controller_routes(api_blueprint, api_routes)
