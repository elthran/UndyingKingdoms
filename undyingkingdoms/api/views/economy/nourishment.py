from flask import jsonify
from flask.views import MethodView
from flask_login import login_required, current_user

class NourishmentAPI(MethodView):
    @login_required
    def get(self):
        county = current_user.county

        return jsonify(
            status='success',
            debugMessage='You called the nourishment api.',
            nourishment=county.nourishment,
            nourishmentChange=county.get_nourishment_change(),
        )
