from flask import jsonify
from flask.views import MethodView
from flask_login import login_required, current_user


class WoodAPI(MethodView):
    @login_required
    def get(self):
        county = current_user.county

        # happinessChange=county.get_happiness_change(),
        # healthinessChange=county.get_healthiness_change(),

        return jsonify(
            status='success',
            message='You called the wood api.',
            wood=county.wood,
            woodIncome=county.get_wood_income(),
            mills=county.buildings['mill'].class_name_plural.title(),
        )
