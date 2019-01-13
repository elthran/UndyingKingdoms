from flask import Blueprint

from .views import AdvanceAPI, TokenAPI

game_clock_blueprint = Blueprint('game_clock', __name__, url_prefix='/game_clock')

game_clock_blueprint.add_url_rule('/advance', view_func=AdvanceAPI.as_view('advance_api'))
game_clock_blueprint.add_url_rule('/token', view_func=TokenAPI.as_view('token_api'))
