from flask import render_template, redirect, url_for, jsonify, request
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from undyingkingdoms import app
from undyingkingdoms.models.forms.economy import EconomyForm
from undyingkingdoms.static.metadata.metadata import rations_terminology, birth_rate_modifier, income_modifier, \
    food_consumed_modifier, happiness_modifier


@app.route('/gameplay/economy/', methods=['GET'])
@mobile_template('{mobile/}dist/economy.html')
@login_required
def economy(template):
    # county = current_user.county
    # kingdom = county.kingdom

    form = EconomyForm(tax=current_user.county.tax, rations=current_user.county.rations)

    form.tax.choices = [(i, i) for i in range(11)]
    form.rations.choices = [(pairing[0], pairing[1]) for pairing in rations_terminology]

    vue_safe_env = app.jinja_env.overlay()
    vue_safe_env.block_start_string = '((*'
    vue_safe_env.block_end_string = '*))'
    vue_safe_env.variable_start_string = '((('
    vue_safe_env.variable_end_string = ')))'
    vue_safe_env.comment_start_string = '((='
    vue_safe_env.comment_end_string = '=))'

    vue_safe_template = vue_safe_env.get_template(template)

    return vue_safe_template.render(
        form=form,
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

    form = EconomyForm(tax=county.tax, rations=county.rations)
    form.tax.choices = [(i, i) for i in range(11)]
    form.rations.choices = [
        (pairing[0], pairing[1])
        for pairing in rations_terminology
    ]

    if form.validate_on_submit():
        county.tax = form.tax.data
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
            happinessChange=county.get_happiness_change(),
            grainStorageChange=county.grain_storage_change(),
            foodEaten=county.get_food_to_be_eaten(),
            nourishmentChange=county.get_nourishment_change()
        )
    return jsonify(
        status="fail",
        message="You economy data did not pass form validation."
    )
