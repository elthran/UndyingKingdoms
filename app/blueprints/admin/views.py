from importlib import import_module

from flask import render_template, request
from flask.views import MethodView
from flask_login import login_required
from flask_mobility.decorators import mobile_template

from app.routes.helpers import admin_required
get_helpers = lambda: import_module('.helpers', __package__)


class HomeAPI(MethodView):
    @mobile_template('{mobile/}user/admin.html')
    @login_required
    @admin_required
    def get(self, template):
        helpers = get_helpers()
        op_code = request.args.get('tool_id', None)
        if op_code:
            if op_code.startswith('bots'):
                return helpers.create_bots(int(op_code.split()[1]))
            elif op_code == 'update_guide':
                return helpers.build_comparison_files()
            elif op_code == 'advance_day':
                return helpers.run_advance_day()
            elif op_code.startswith('example'):
                return "execute and return an example function as json"
            else:
                return None
        return render_template(template)

    @login_required
    @admin_required
    def post(self):
        helpers = get_helpers()
        if request.is_json:
            data = request.get_json()
            op_code = data.get('tool_id', None)
            if op_code == 'notification':
                message = data.get("message", "Error: missing key")
                return helpers.create_notification(message)
        return None
