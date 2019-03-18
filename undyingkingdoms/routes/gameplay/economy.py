from flask import render_template, redirect, url_for, jsonify, request, send_from_directory, current_app
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from undyingkingdoms import app
from undyingkingdoms.models.forms.economy import EconomyForm
from undyingkingdoms.static.metadata.metadata import rations_terminology, birth_rate_modifier, income_modifier, \
    food_consumed_modifier, happiness_modifier, tax_options


@app.route('/gameplay/economy/', methods=['GET'])
@mobile_template('{mobile/}gameplay/economy.html')
@login_required
def economy(template):
    form = EconomyForm(tax=current_user.county.tax_rate, rations=current_user.county.rations)

    form.tax.choices = tax_options
    form.rations.choices = rations_terminology

    return render_template(
        template,
        form=form,
        birth_rate_modifier=birth_rate_modifier,
        income_modifier=income_modifier,
        food_consumed_modifier=food_consumed_modifier,
        happiness_modifier=happiness_modifier)
    # return send_from_directory('static/dist', 'economy.html')


@app.route('/gameplay/economy/update', methods=['POST'])
@login_required
def update_economy():
    """Update the economy page with new data.

    taxes affects: gold in 3 places and happiness 2 places.
    rations affects: food and healthiness.
        food in 2 places, healthiness in 1.
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
            message="You have updated your economy data.",
            birth_rate_modifier=birth_rate_modifier,
            income_modifier=income_modifier,
            food_consumed_modifier=food_consumed_modifier,
            happiness_modifier=happiness_modifier,
            goldChange=county.get_gold_change(),
            taxIncome=county.get_tax_income(),
            happinessChange=county.get_happiness_change(),
            grainStorageChange=county.grain_storage_change(),
            foodEaten=county.get_food_to_be_eaten(),
            healthinessChange=county.get_healthiness_change()
        )
    return jsonify(
        status="fail",
        message="You economy data did not pass form validation."
    )
