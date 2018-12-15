from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from undyingkingdoms import app, db
from undyingkingdoms.models.forms.economy import EconomyForm
from undyingkingdoms.static.metadata import rations_terminology


@login_required
@app.route('/gameplay/economy/', methods=['GET', 'POST'])
def economy():
    form = EconomyForm(tax=current_user.county.tax, rations=current_user.county.rations)
    form.tax.choices = [(i, i) for i in range(11)]
    form.rations.choices = [(pairing[0], pairing[1]) for pairing in rations_terminology]
    if form.validate_on_submit():
        current_user.county.tax = form.tax.data
        current_user.county.rations = form.rations.data
        db.session.commit()
        return redirect(url_for('economy'))
    return render_template('gameplay/economy.html', form=form)
