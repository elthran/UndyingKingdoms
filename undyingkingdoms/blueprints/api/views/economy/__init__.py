from ... import api_blueprint
from .popluation import PopulationAPI
from .gold import GoldAPI

prefix = 'economy'
url = f'/{prefix}'
view = f'{prefix}_'

api_blueprint.add_url_rule(
    f'{url}/population',
    view_func=PopulationAPI.as_view(f'{view}population_api')
)
api_blueprint.add_url_rule(
    f'{url}/gold',
    view_func=GoldAPI.as_view(f'{view}gold_api')
)
