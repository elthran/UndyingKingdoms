from flask import jsonify
from flask.views import MethodView
from flask_login import login_required, current_user

class HealthinessAPI(MethodView):
    @login_required
    def get(self):
        county = current_user.county

        return jsonify(
            status='success',
            message='You called the healthiness api.',
            healthiness=county.healthiness,
            healthinessChange=county.get_healthiness_change(),
        )
