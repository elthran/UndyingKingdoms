from importlib import import_module

from utilities.helpers import to_class_name
from .helpers import import_endpoints
from .. import api_blueprint

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
