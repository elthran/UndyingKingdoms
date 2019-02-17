from flask import render_template, redirect, url_for, jsonify, request
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from undyingkingdoms import app
from undyingkingdoms.models.forms.economy import EconomyForm
from undyingkingdoms.models.preferences import Preferences
from undyingkingdoms.static.metadata.metadata import rations_terminology, birth_rate_modifier, income_modifier, \
    food_consumed_modifier, happiness_modifier


@app.route('/gameplay/economy/', methods=['GET'])
@mobile_template('{mobile/}gameplay/economy.html')
@login_required
def economy(template):
    county_preferences = Preferences.query.filter_by(county_id=current_user.county.id).first()
    tax_rate = county_preferences.tax_rate
    rations = county_preferences.rations
    form = EconomyForm(tax=tax_rate, rations=rations)

    form.tax.choices = [(i, i) for i in range(11)]
    form.rations.choices = [(pairing[0], pairing[1]) for pairing in rations_terminology]

    return render_template(
        template, form=form,
        birth_rate_modifier=birth_rate_modifier,
        income_modifier=income_modifier,
        food_consumed_modifier=food_consumed_modifier,
        happiness_modifier=happiness_modifier)


@app.route('/gameplay/economy/update', methods=['POST'])
@login_required
def update_economy():
    """Update the economy page with new data.

    taxes affects: gold in 3 places and happiness 2 places.
    rations affects: food and nourishment.
        food in 2 places, nourishment in 1.
    """
    county = current_user.county
    county_preferences = Preferences.query.filter_by(county_id=county.id).first()
    tax_rate = county_preferences.tax_rate
    rations = county_preferences.rations

    form = EconomyForm(tax=tax_rate, rations=rations)
    form.tax.choices = [(i, i) for i in range(11)]
    form.rations.choices = [
        (pairing[0], pairing[1])
        for pairing in rations_terminology
    ]

    if form.validate_on_submit():
        county_preferences.tax_rate = form.tax.data
        county_preferences.rations = form.rations.data

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
            happinessChange=county.get_happiness_change(),
            grainStorageChange=county.grain_storage_change(),
            foodEaten=county.get_food_to_be_eaten(),
            nourishmentChange=county.get_nourishment_change()
        )
    return jsonify(
        status="fail",
        message="You economy data did not pass form validation."
    )
