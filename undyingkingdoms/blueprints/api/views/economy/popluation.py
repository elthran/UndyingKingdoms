from flask import jsonify
from flask.views import MethodView
from flask_login import login_required, current_user


class PopulationAPI(MethodView):
    @login_required
    def get(self):
        county = current_user.county

        return jsonify(
            status='success',
            message='You called on the population api.',
            population=county.population,
        )
