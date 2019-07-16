from flask import jsonify
from flask.views import MethodView
from flask_login import login_required, current_user


class TreasuryAPI(MethodView):
    @login_required
    def get(self):
        county = current_user.county

        return jsonify(
            status="success",
            debugMessage=f"You called on {__name__}",
            gold=county.gold,
            wood=county.wood,
            iron=county.iron,
            stone=county.stone,
            mana=county.mana
        )
