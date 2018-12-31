from flask import Blueprint

from .views.refresh import RefreshAPI
from .views.reset import ResetAPI
from .views.export import ExportAPI

admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin')

# add rule for API endpoints
admin_blueprint.add_url_rule('/refresh', view_func=RefreshAPI.as_view('refresh_api'))
admin_blueprint.add_url_rule('/reset', view_func=ResetAPI.as_view('reset_api'))
admin_blueprint.add_url_rule('/export', view_func=ExportAPI.as_view('export_api'))


@admin_blueprint.route("/")
def home():
    return "Admin page that needs a fancy template panel for all these nice functions."
