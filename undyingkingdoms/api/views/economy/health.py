from flask import jsonify
from flask.views import MethodView
from flask_login import login_required, current_user

class HealthAPI(MethodView):
    @login_required
    def get(self):
        county = current_user.county

        return jsonify(
            status='success',
            debugMessage='You called the health api.',
            health=county.health,
            healthChange=county.get_health_change(),
            healthTerminology=county.health_terminology.title(),
        )
