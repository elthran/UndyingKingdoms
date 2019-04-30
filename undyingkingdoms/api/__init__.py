from importlib import import_module

from flask import Blueprint

from extensions import flask_csrf
from utilities.helpers import to_class_name

api_blueprint = Blueprint('api', __name__, url_prefix='/api')
flask_csrf.exempt(api_blueprint)

from . import chatroom
from . import forum
from . import infrastructure
from . import overview
from . import research

endpoints = {
    'sidebar': None,
    'routing': {
        'path_args': '/<route>'
    },
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
