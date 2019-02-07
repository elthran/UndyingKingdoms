from flask import Blueprint, url_for
from werkzeug.utils import redirect

from .views.home import HomeAPI
# from .views.reset import ResetAPI

admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin')

# add rule for API endpoints
admin_blueprint.add_url_rule('/home', view_func=HomeAPI.as_view('home_api'))


@admin_blueprint.route("/")
def admin():
    """An administrative panel allowing various database functions."""

    return redirect(url_for('admin.home_api'))
