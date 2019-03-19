from flask import jsonify
from flask.views import MethodView
from flask_login import login_required, current_user

class CitizensAPI(MethodView):
    @login_required
    def get(self):
        county = current_user.county

        return jsonify(
            status="success",
            message=f"You called on {__name__}",
            population=county.population,
            happiness_term=county.happiness_terminology.title(),
            healthiness_term=county.healthiness_terminology.title(),
            grain_stores=county.grain_stores
        )
