from flask import jsonify
from flask.views import MethodView
from flask_login import login_required, current_user

from undyingkingdoms.jinja_filters import vue_safe
from undyingkingdoms.models.forms.economy import EconomyForm
from undyingkingdoms.static.metadata.metadata import rations_terminology, birth_rate_modifier, income_modifier, \
    food_consumed_modifier, happiness_modifier, tax_options


class GoldAPI(MethodView):
    @login_required
    def get(self):
        county = current_user.county

        # overwrite and vueify form, probably should be a method.
        form = EconomyForm(tax=current_user.county.tax, rations=current_user.county.rations)

        # fake form
        form = dict(
            tax=dict(
                choices=vue_safe(tax_options, for_template=False),
                ID=form.tax.id
            ),
            rations=dict(
                choices=vue_safe(rations_terminology, for_template=False),
                ID=form.rations.id
            )
        )

        data = dict(
            tax=county.tax,
            gold=county.gold,
            rations=county.rations,
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
