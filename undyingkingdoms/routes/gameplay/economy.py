from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from undyingkingdoms import app
from undyingkingdoms.models.forms.economy import EconomyForm
from undyingkingdoms.static.metadata import rations_terminology, birth_rate_modifier, income_modifier


@app.route('/gameplay/economy/', methods=['GET', 'POST'])
@mobile_template('{mobile/}gameplay/economy.html')
@login_required
def economy(template):
    if not current_user.in_active_session:
        current_user.in_active_session = True
    form = EconomyForm(tax=current_user.county.tax, rations=current_user.county.rations)
    form.tax.choices = [(i, i) for i in range(11)]
    form.rations.choices = [(pairing[0], pairing[1]) for pairing in rations_terminology]
    if form.validate_on_submit():
        current_user.county.tax = form.tax.data
        current_user.county.rations = form.rations.data
        return redirect(url_for('economy'))
    return render_template(template, form=form, birth_rate_modifier=birth_rate_modifier, income_modifier=income_modifier)
