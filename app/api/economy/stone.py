from flask import jsonify
from flask.views import MethodView
from flask_login import login_required, current_user


class StoneAPI(MethodView):
    @login_required
    def get(self):
        county = current_user.county
        infrastructure = county.infrastructure

        return jsonify(
            status='success',
            debugMessage='You called the stone api.',
            stoneAmount=county.stone,
            stoneIncome=infrastructure.get_stone_income(),
            descriptiveName=infrastructure.buildings['quarry'].class_name_plural.title(),
        )
