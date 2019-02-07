from flask import render_template, request
from flask.views import MethodView
from flask_login import login_required
from flask_mobility.decorators import mobile_template

from ..helpers import create_bots
from undyingkingdoms.routes.helpers import in_active_session, admin_required


class HomeAPI(MethodView):
    @mobile_template('{mobile/}user/admin.html')
    @login_required
    @in_active_session
    @admin_required
    def get(self, template):
        op_code = request.args.get('tool_id', None)
        if op_code:
            if op_code.startswith('bots'):
                return create_bots(int(op_code.split()[1]))

            print(op_code)

        return render_template(template)
