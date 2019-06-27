from flask import jsonify
from flask.views import MethodView
from flask_login import login_required, current_user

from .helpers import troop_sum
from ..vue_safe import generic_vue_safe


class UpdateAPI(MethodView):
    @login_required
    def get(self):
        county = current_user.county

        expeditions = county.get_expeditions()

        json_expeditions = [
            generic_vue_safe(
                expedition,
                [
                    'success',
                    'duration',
                    'land_acquired',
                    'land_razed',
                    'gold_gained',
                    'iron_gained',
                    'wood_gained',
                ],
                troops=troop_sum(expedition),
            )
            for expedition in expeditions
        ]
        return jsonify(
            debugMessage=f"You called on {__name__}",
            expeditions=json_expeditions
        )
