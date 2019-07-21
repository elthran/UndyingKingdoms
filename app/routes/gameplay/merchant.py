from importlib import import_module

from flask import render_template, url_for, redirect
from flask_login import login_required, current_user

from app import app
get_forms = lambda: import_module('app.models.forms.exports')


@app.route('/gameplay/merchant', methods=['GET', 'POST'])
@login_required
def merchant():
    forms = get_forms()
    county = current_user.county

    form = forms.MerchantForm()
    form.county_id.data = county.id

    resources = ['stone', 'iron', 'wood', 'gold', 'food']

    form.offer_resource.choices = [(i, resources[i]) for i in range(len(resources))]
    form.offer.choices = [(i, i) for i in range(50)]
    form.receive_resource.choices = [(i, resources[i]) for i in range(len(resources))]

    if form.validate_on_submit():

        resource_map = {0: 'stone', 1: 'iron', 2: 'wood', 3: 'gold', 4: 'grain_stores'}
        offer_type = form.offer_resource.data
        offer_amount = form.offer.data
        old_value = getattr(county, resource_map[offer_type])
        setattr(county, resource_map[offer_type], old_value - offer_amount)

        receive_type = form.receive_resource.data
        receive_amount = int(form.receive.data)
        old_value = getattr(county, resource_map[receive_type])
        setattr(county, resource_map[receive_type], old_value + receive_amount)

        return redirect(url_for('merchant'))

    return render_template('gameplay/merchant.html', form=form)
