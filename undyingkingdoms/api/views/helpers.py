from importlib import import_module


def to_class_name(name):
    return ''.join(name.title().split('_'))


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
    """

    # undyingkingdoms.api.views.infrastructure -> infrastructure
    folder = mod_name.split('.')[-1]
    for endpoint in endpoints:
        mod = import_module('.' + endpoint, mod_name)
        class_name = to_class_name(endpoint) + 'API'
        Class = getattr(mod, class_name)
        blueprint.add_url_rule(
            f'/{folder}/{endpoint}',
            view_func=Class.as_view(f'{folder}_{endpoint}_api')
        )
