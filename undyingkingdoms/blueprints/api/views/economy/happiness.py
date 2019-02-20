from flask import jsonify
from flask.views import MethodView
from flask_login import login_required, current_user


class HappinessAPI(MethodView):
    @login_required
    def get(self):
        county = current_user.county

        return jsonify(
            status='success',
            message='You called the happiness api.',
            happiness=county.happiness,
            happinessChange=county.get_happiness_change(),
        )
