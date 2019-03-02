from flask import jsonify
from flask.views import MethodView
from flask_login import login_required, current_user


class ResourcesAPI(MethodView):
    @login_required
    def get(self):
        county = current_user.county

        return jsonify(
            status="success",
            message="You called on the resources api.",
            availableLand=county.get_available_land(),
            availableCitizens=county.get_available_workers(),
            land=county.land,
            population=county.population,
            gold=county.gold,
            wood=county.wood,
            iron=county.iron,
            stone=county.stone,
            buildSlots=county.get_number_of_buildings_produced_per_day()
        )
