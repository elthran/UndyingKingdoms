from flask import jsonify
from flask.views import MethodView
from flask_login import login_required, current_user

from undyingkingdoms.jinja_filters import vue_safe
from undyingkingdoms.models.forms.economy import EconomyForm
from undyingkingdoms.static.metadata.metadata import rations_terminology, birth_rate_modifier, income_modifier, \
    food_consumed_modifier, happiness_modifier


class GoldAPI(MethodView):
    @login_required
    def get(self):
        county = current_user.county

        form = EconomyForm(tax=current_user.county.tax, rations=current_user.county.rations)

        form.tax.choices = [(i, i) for i in range(11)]
        form.rations.choices = [(pairing[0], pairing[1]) for pairing in rations_terminology]
        # vue_safe()

        data = dict(
            goldChange=county.get_gold_change(),
            happinessChange=county.get_happiness_change(),
            grainStorageChange=county.grain_storage_change(),
            foodEaten=county.get_food_to_be_eaten(),
            nourishmentChange=county.get_nourishment_change()
        )

        return jsonify(
            status='success',
            message='You called on the gold api.',
            county=data,
            form=form,
            birth_rate_modifier=birth_rate_modifier,
            income_modifier=income_modifier,
            food_consumed_modifier=food_consumed_modifier,
            happiness_modifier=happiness_modifier,
        )
