from flask import jsonify
from flask.views import MethodView
from flask_login import login_required, current_user


class StoneAPI(MethodView):
    @login_required
    def get(self):
        county = current_user.county

        return jsonify(
            status='success',
            message='You called the stone api.',
            stoneAmount=county.stone,
            stoneIncome=county.get_stone_income(),
            quarries=county.buildings['quarry'].class_name_plural.title(),
        )
