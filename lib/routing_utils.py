from functools import wraps
from importlib import import_module

from lib.namers import to_class_name, to_endpoint_name


def attach_controller_routes(blueprint, routes):
    """Attach routes from a specialized dictionary.

    Format should be:
    routes = {
        '/infrastructure': {
            GET: InfrastructureController.read,
            PUT: InfrastructureController.update
        },
        '/routing/<route>': {
            GET: RoutingController.read,
        }
    }
    """
    for route, endpoints in routes.items():
        for verb, controller in endpoints.items():
            # if 'Navbar' in controller.__qualname__: breakpoint()
            view_func = build_view_function(controller)
            blueprint.add_url_rule(
                route,
                endpoint=to_endpoint_name(controller.__qualname__),
                view_func=view_func,
                methods=[verb]
            )
    return blueprint


def build_view_function(controller):
    """Convert a method into an actual view function for the routing system.

    Internally generates an instance of the class on the fly so as to
    fill the self parameter.
    """
    module = import_module(controller.__module__)
    cls_name, *_, = controller.__qualname__.split('.')
    cls = getattr(module, cls_name)

    @wraps(controller)
    def as_view(*args, **kwargs):
        return controller(cls(), *args, **kwargs)

    return as_view


def import_endpoints(blueprint, mod_name, endpoints):
    """Generically add all routes.

    mod_name == __name__ (of the calling package)
    e.g.
    from .population import PopulationAPI

    api_blueprint.add_url_rule(
        f'/economy/population',
        view_func=PopulationAPI.as_view(f'economy_population_api')

    Access looks like:
        js - http.get('/api/economy/population')
        python - url_for('api.economy_population_api')
        (someday, url_for('api.economy.population'))

    Note: endpoints can now be a dictionary with optional path arguments.
    {
        'messaging': None,
        'upvote': {
            'path_ags': '/<int:post_id>'
        },
    }
    Produces:
        js - http.get('/api/economy/population/n')
        python - url_for('api.economy_population_api', post_id=n)
    """

    # app.api.views.infrastructure -> infrastructure
    folder = mod_name.split('.')[-1]
    for endpoint in endpoints:
        mod = import_module('.' + endpoint, mod_name)
        class_name = to_class_name(endpoint) + 'API'
        Class = getattr(mod, class_name)
        try:  # add optional path arguments
            path = endpoints[endpoint]['path_args']
        except (KeyError, TypeError):
            path = ''
        blueprint.add_url_rule(
            f'/{folder}/{endpoint}{path}',
            view_func=Class.as_view(f'{folder}_{endpoint}_api')
        )
