from flask import render_template, url_for, redirect
from flask_login import login_required, current_user

from undyingkingdoms import app
from undyingkingdoms.models.forms.merchant import MerchantForm


@app.route('/gameplay/merchant', methods=['GET', 'POST'])
@login_required
def merchant():

    county = current_user.county

    form = MerchantForm()

    resources = ['stone', 'iron', 'wood', 'gold', 'food']

    form.offer_resource.choices = [(i, resources[i]) for i in range(len(resources))]
    form.offer.choices = [(i, i) for i in range(50)]
    form.receive_resource.choices = [(i, resources[i]) for i in range(len(resources))]
    form.receive.choices = [(i, i) for i in range(50)]

    if form.validate_on_submit():

        print("This trade should give you {} {} and you will lose {} {}".format(
            form.receive.data,
            form.receive_resource.data,
            form.offer.data,
            form.offer_resource.data))

        offer_type = form.offer_resource.data
        offer_amount = form.offer.data
        old_value = getattr(county, offer_type)
        setattr(county, offer_type, old_value - offer_amount)

        receive_type = form.receive_resource.data
        receive_amount = form.receive.data
        old_value = getattr(county, receive_type)
        setattr(county, receive_type, old_value + receive_amount)

        return redirect(url_for('merchant'))

    return render_template('gameplay/merchant.html', form=form)
