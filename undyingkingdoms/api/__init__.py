from flask import Blueprint

from extensions import flask_csrf

api_blueprint = Blueprint('api', __name__, url_prefix='/api')
flask_csrf.exempt(api_blueprint)

from . import views
from .views import infrastructure
from .views import overview
from .views import chatroom
from .views import forum
