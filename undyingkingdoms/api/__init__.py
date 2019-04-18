from flask import Blueprint

from extensions import flask_csrf
from .views.sidebar import SideBarAPI

api_blueprint = Blueprint('api', __name__, url_prefix='/api')
flask_csrf.exempt(api_blueprint)

api_blueprint.add_url_rule('/sidebar', view_func=SideBarAPI.as_view('sidebar_api'))

# from .views import economy
from .views import infrastructure
from .views import overview
from .views import chatroom
from .views import forum
