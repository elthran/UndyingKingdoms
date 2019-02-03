from flask import Blueprint

from .views.advance_day import AdvanceDayAPI
from .views.token import TokenAPI
from .views.advance_24h_analytics import Advance24hAnalyticsAPI
from .views.advance_age import AdvanceAgeAPI
from .views.close_inactive_sessions import CloseInactiveSessionsAPI

game_clock_blueprint = Blueprint('game_clock', __name__, url_prefix='/game_clock')

game_clock_blueprint.add_url_rule('/advance_day', view_func=AdvanceDayAPI.as_view('advance_day_api'))
game_clock_blueprint.add_url_rule('/token', view_func=TokenAPI.as_view('token_api'))
game_clock_blueprint.add_url_rule('/advance_24h_analytics', view_func=Advance24hAnalyticsAPI.as_view('advance_24h_analytics_api'))
game_clock_blueprint.add_url_rule('/advance_age', view_func=AdvanceAgeAPI.as_view('advance_age_api'))
game_clock_blueprint.add_url_rule('/close_inactive_sessions', view_func=CloseInactiveSessionsAPI.as_view('close_inactive_sessions_api'))
