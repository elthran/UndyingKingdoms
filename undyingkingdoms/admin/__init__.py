from flask import Blueprint, render_template

# from .views.refresh import RefreshAPI
# from .views.reset import ResetAPI

admin_blueprint = Blueprint(
    'admin',
    __name__,
    url_prefix='/admin',
    template_folder='templates',
    static_folder='static'
)

# add rule for API endpoints
# admin_blueprint.add_url_rule('/refresh', view_func=RefreshAPI.as_view('refresh_api'))
# admin_blueprint.add_url_rule('/reset', view_func=ResetAPI.as_view('reset_api'))


@admin_blueprint.route("/")
def admin():
    """An administrative panel allowing various database functions."""

    return render_template('admin.html')
