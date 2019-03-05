from importlib import import_module

from ..helpers import to_class_name
from ... import api_blueprint

__doc__ = """
Generically add all routes.

e.g.
from .population import PopulationAPI

api_blueprint.add_url_rule(
    f'/economy/population',
    view_func=PopulationAPI.as_view(f'economy_population_api')
"""

endpoints = ['resources', 'idle_population']

for endpoint in endpoints:
    mod = import_module('.' + endpoint, __name__)
    class_name = to_class_name(endpoint) + 'API'
    Class = getattr(mod, class_name)
    api_blueprint.add_url_rule(
        f'/infrastructure/{endpoint}',
        view_func=Class.as_view(f'infrastructure_{endpoint}_api')
    )

