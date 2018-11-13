from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from undyingkingdoms import app, db
from undyingkingdoms.models.forms.economy import EconomyForm


@login_required
@app.route('/gameplay/economy/', methods=['GET', 'POST'])
def economy():
    form = EconomyForm(tax=current_user.county.tax)
    form.tax.choices = [(i, i) for i in range(21)]
    if form.validate_on_submit():
        current_user.county.tax = form.tax.data
        db.session.commit()
        return redirect(url_for('economy'))
    return render_template('gameplay/economy.html', form=form)
