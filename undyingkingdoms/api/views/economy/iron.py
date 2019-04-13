from flask import jsonify
from flask.views import MethodView
from flask_login import login_required, current_user


class IronAPI(MethodView):
    @login_required
    def get(self):
        county = current_user.county

        return jsonify(
            status='success',
            debugMessage='You called the iron api.',
            iron=county.iron,
            ironIncome=county.get_iron_income(),
            mines=county.buildings['mine'].class_name_plural.title(),
        )
