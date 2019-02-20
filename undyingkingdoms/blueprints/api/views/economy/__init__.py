from ... import api_blueprint
from .popluation import PopulationAPI
from .gold import GoldAPI
from .food import FoodAPI

prefix = 'economy'
url = f'/{prefix}'
view = f'{prefix}_'

# e.g. /economy/population
# economy_population_api
api_blueprint.add_url_rule(
    f'{url}/population',
    view_func=PopulationAPI.as_view(f'{view}population_api')
)
api_blueprint.add_url_rule(
    f'{url}/gold',
    view_func=GoldAPI.as_view(f'{view}gold_api')
)

api_blueprint.add_url_rule(
    f'{url}/food',
    view_func=FoodAPI.as_view(f'{view}food_api')
)
