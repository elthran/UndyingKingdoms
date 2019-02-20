from importlib import import_module

from ... import api_blueprint

__doc__ = """
Generically add all routes.

e.g.
from .population import PopulationAPI

api_blueprint.add_url_rule(
    f'/economy/population',
    view_func=PopulationAPI.as_view(f'economy_population_api')
"""

endpoints = ['population', 'gold', 'food', 'wood', 'iron', 'stone', 'mana',
             'happiness', 'nourishment', 'health']

for endpoint in endpoints:
    mod = import_module('.' + endpoint, __name__)
    class_name = endpoint.title() + 'API'
    Class = getattr(mod, class_name)
    api_blueprint.add_url_rule(
        f'/economy/{endpoint}',
        view_func=Class.as_view(f'economy_{endpoint}_api')
    )

