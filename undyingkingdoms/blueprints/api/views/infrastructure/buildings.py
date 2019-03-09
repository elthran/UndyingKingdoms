from flask import jsonify, url_for
from flask.views import MethodView
from flask_login import login_required, current_user

class BuildingsAPI(MethodView):
    @login_required
    def get(self):
        county = current_user.county

        buildingsChoices = [[i, building.class_name.title()] for i, building in enumerate(county.buildings.values())]


        return jsonify(
            status="success",
            message="You called on the buildings api.",
            buildingsChoices=buildingsChoices
        )
