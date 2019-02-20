from flask import jsonify
from flask.views import MethodView
from flask_login import login_required, current_user

from undyingkingdoms.blueprints.api.vue_safe import vue_safe_form, vue_safe_metadata_mod
from undyingkingdoms.models.forms.economy import EconomyForm
from undyingkingdoms.static.metadata.metadata import tax_options, rations_terminology, food_consumed_modifier


class FoodAPI(MethodView):
    @login_required
    def get(self):
        county = current_user.county

        # probably should move to a function.
        form = EconomyForm(tax=current_user.county.tax, rations=current_user.county.rations)
        form.tax.choices = tax_options
        form.rations.choices = rations_terminology

        # happinessChange=county.get_happiness_change(),
        # nourishmentChange=county.get_nourishment_change(),

#         { % if food_consumed_modifier.get(county.race)[1] %}
#         {{food_consumed_modifier.get(county.race)[0]}}: {{
#             (food_consumed_modifier.get(county.race)[1] * 100) |}} % < span
#         class ="tooltipText" >
#         Racial
#         Modifier: {{county.race}}

        return jsonify(
            status='success',
            message='You called the food api.',
            grain_stores=county.grain_stores,
            grainStorageChange=county.grain_storage_change(),
            foodEaten=county.get_food_to_be_eaten(),
            rations=county.rations,
            form=vue_safe_form(form),
            race=county.race,
            background=county.background,
            food_consumed_mod=vue_safe_metadata_mod(food_consumed_modifier, county),
            producedGrain=county.get_produced_grain(),
            producedDairy=county.get_produced_dairy(),
            isForaging=county.production_choice == 2,
            excessProduction=county.get_excess_production_value(2),
        )
