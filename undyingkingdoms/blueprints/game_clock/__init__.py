from flask import Blueprint

from .views.advance import AdvanceAPI
from .views.token import TokenAPI
from .views.advance_24h_analytics import Advance24hAnalyticsAPI

game_clock_blueprint = Blueprint('game_clock', __name__, url_prefix='/game_clock')

game_clock_blueprint.add_url_rule('/advance', view_func=AdvanceAPI.as_view('advance_api'))
game_clock_blueprint.add_url_rule('/token', view_func=TokenAPI.as_view('token_api'))
game_clock_blueprint.add_url_rule('/advance_24h_analytics', view_func=TokenAPI.as_view('advance_24h_analytics_api'))
