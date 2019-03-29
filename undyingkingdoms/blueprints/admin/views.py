from flask import render_template, request, current_app
from flask.views import MethodView
from flask_login import login_required
from flask_mobility.decorators import mobile_template

from undyingkingdoms.blueprints.admin.helpers import create_bots, create_notification, build_comparison_files, \
    run_advance_day
from undyingkingdoms.routes.helpers import admin_required


class HomeAPI(MethodView):
    @mobile_template('{mobile/}user/admin.html')
    @login_required
    @admin_required
    def get(self, template):
        op_code = request.args.get('tool_id', None)
        if op_code:
            if op_code.startswith('bots'):
                return create_bots(int(op_code.split()[1]))
            elif op_code == 'update_guide':
                return build_comparison_files()
            elif op_code == 'advance_day':
                return run_advance_day()
            elif op_code.startswith('example'):
                return "execute and return an example function as json"
            else:
                return None
        return render_template(
            template,
            is_production=current_app.config['ENV'] == 'production'
        )

    @login_required
    @admin_required
    def post(self):
        if request.is_json:
            data = request.get_json()
            op_code = data.get('tool_id', None)
            if op_code == 'notification':
                message = data.get("message", "Error: missing key")
                return create_notification(message)
        return None
