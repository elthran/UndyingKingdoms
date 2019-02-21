from flask import request, url_for, jsonify
from flask.views import MethodView
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from undyingkingdoms.blueprints.api.vue_safe import vue_safe_form
from undyingkingdoms.models.forms.economy import EconomyForm
from undyingkingdoms.static.metadata.metadata import rations_terminology, tax_options


class UpdateAPI(MethodView):
    @login_required
    def get(self):
        county = current_user.county

        form = EconomyForm(tax=county.tax_rate, rations=county.rations)
        form.tax.choices = tax_options
        form.rations.choices = rations_terminology

        return jsonify(
            status="success",
            message="You have accessed the update api.",
            form=vue_safe_form(form)
        )


    @login_required
    def post(self):
        """Update the economy page with new data.

        taxes affects: gold in 3 places and happiness 2 places.
        rations affects: food and nourishment.
            food in 2 places, nourishment in 1.
        """
        county = current_user.county

        form = EconomyForm(tax=county.tax_rate, rations=county.rations)
        form.tax.choices = tax_options
        form.rations.choices = rations_terminology


        if form.validate_on_submit():
            county.tax_rate = form.tax.data
            county.rations = form.rations.data

            # Because I'm too lazy to update the mobile page right now.
            if getattr(request, 'MOBILE', None):
                return redirect(url_for('economy'))

            return jsonify(
                status="success",
                message="You have submitted your economy form.",
                # birth_rate_modifier=birth_rate_modifier,
                # income_modifier=income_modifier,
                # food_consumed_modifier=food_consumed_modifier,
                # happiness_modifier=happiness_modifier,
                # goldChange=county.get_gold_change(),
                # taxIncome=county.get_tax_income(),
                # happinessChange=county.get_happiness_change(),
                # grainStorageChange=county.grain_storage_change(),
                # foodEaten=county.get_food_to_be_eaten(),
                # nourishmentChange=county.get_nourishment_change()
            )
        return jsonify(
            status="fail",
            message="You economy data did not pass form validation."
        )
