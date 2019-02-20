from flask import jsonify
from flask.views import MethodView
from flask_login import login_required, current_user

from ...vue_safe import vue_safe_metadata_mod, vue_safe_form
from undyingkingdoms.models.forms.economy import EconomyForm
from undyingkingdoms.static.metadata.metadata import rations_terminology, income_modifier, tax_options


class GoldAPI(MethodView):
    @login_required
    def get(self):
        county = current_user.county

        # overwrite and vueify form, probably should be a method.
        form = EconomyForm(tax=current_user.county.tax, rations=current_user.county.rations)
        form.tax.choices = tax_options
        form.rations.choices = rations_terminology

        return jsonify(
            status='success',
            message='You called on the gold api.',
            tax=county.tax,
            gold=county.gold,
            rations=county.rations,
            goldChange=county.get_gold_change(),
            happinessChange=county.get_happiness_change(),
            grainStorageChange=county.grain_storage_change(),
            foodEaten=county.get_food_to_be_eaten(),
            nourishmentChange=county.get_nourishment_change(),
            form=vue_safe_form(form),
            income_mod=vue_safe_metadata_mod(income_modifier, county),
            race=county.race,
            background=county.background
        )
