from flask import jsonify
from flask.views import MethodView
from flask_login import login_required, current_user

from ...vue_safe import vue_safe_metadata_mod
from undyingkingdoms.static.metadata.metadata import happiness_modifier


class HappinessAPI(MethodView):
    @login_required
    def get(self):
        county = current_user.county

        return jsonify(
            status='success',
            debugMessage='You called the happiness api.',
            happiness=county.happiness,
            happinessChange=county.get_happiness_change(),
            areRelaxing=county.production_choice == 3,
            excessProduction=county.get_excess_production_value(3),
            happinessMod=vue_safe_metadata_mod(happiness_modifier, county, is_percent=False),
            race=county.race,
            background=county.background,
            taxRate=county.tax_rate
        )
