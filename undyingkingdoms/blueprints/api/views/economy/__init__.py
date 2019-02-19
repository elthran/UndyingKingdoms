from ... import api_blueprint
from .popluation import PopulationAPI

prefix = '/economy'

api_blueprint.add_url_rule(prefix+'/population', view_func=PopulationAPI.as_view('population_api'))
