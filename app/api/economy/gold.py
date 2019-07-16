from flask import jsonify
from flask.views import MethodView
from flask_login import login_required, current_user

from app.serializers.vue_safe import vue_safe_metadata_mod, vue_safe_form
from app.models.forms.economy import EconomyForm
from app.metadata.metadata import income_modifier, tax_options


class GoldAPI(MethodView):
    @login_required
    def get(self):
        county = current_user.county

        # overwrite and vueify form, probably should be a method.
        form = EconomyForm(tax=county.tax_rate)
        form.tax.choices = tax_options

        return jsonify(
            status='success',
            debugMessage='You called on the gold api.',
            tax=county.tax_rate,
            gold=county.gold,
            rations=county.rations,
            goldChange=county.gold_income,
            form=vue_safe_form(form),
            income_mod=vue_safe_metadata_mod(income_modifier, county),
            race=county.race,
            background=county.background,
            taxIncome=county.get_tax_income(),
            bankIncome=county.bank_income,
            hasBanks=county.buildings['bank'].total > 0,
            isOverworking=county.production_choice == 0,
            excessProduction=county.get_excess_production_value(0),
            militaryExpenses=county.get_upkeep_costs(),
        )
