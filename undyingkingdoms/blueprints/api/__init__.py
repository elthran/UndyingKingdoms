from flask import Blueprint

from extensions import flask_csrf
from undyingkingdoms.blueprints.api.views.sidebar import SideBarAPI

api_blueprint = Blueprint('api', __name__, url_prefix='/api')
flask_csrf.exempt(api_blueprint)

api_blueprint.add_url_rule('/sidebar', view_func=SideBarAPI.as_view('sidebar_api'))
