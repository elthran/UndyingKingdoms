from flask import jsonify
from flask.views import MethodView
from flask_login import login_required, current_user


class WoodAPI(MethodView):
    @login_required
    def get(self):
        county = current_user.county
        infrastructure = county.infrastructure

        # happinessChange=county.happiness_change,
        # nourishmentChange=county.get_nourishment_change(),

        return jsonify(
            status='success',
            debugMessage='You called the wood api.',
            wood=county.wood,
            woodIncome=infrastructure.get_wood_income(),
            mills=infrastructure.buildings['mill'].class_name_plural.title(),
        )
