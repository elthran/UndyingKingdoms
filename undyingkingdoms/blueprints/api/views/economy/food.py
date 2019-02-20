from flask import jsonify
from flask.views import MethodView
from flask_login import login_required, current_user


class FoodAPI(MethodView):
    @login_required
    def get(self):
        county = current_user.county

        # happinessChange=county.get_happiness_change(),

        return jsonify(
            grain_stores=county.grain_stores,
            grainStorageChange=county.grain_storage_change(),
            foodEaten=county.get_food_to_be_eaten(),
            nourishmentChange=county.get_nourishment_change(),
        )
