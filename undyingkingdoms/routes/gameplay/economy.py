from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from undyingkingdoms import app, db
from undyingkingdoms.models.forms.economy import EconomyForm

rations_choices = ["None", "Quarter", "Half", "Normal", "Double", "Triple"]

@login_required
@app.route('/gameplay/economy/', methods=['GET', 'POST'])
def economy():
    form = EconomyForm(tax=current_user.county.tax, rations=current_user.county.rations)
    form.tax.choices = [(i, i) for i in range(21)]
    form.rations.choices = [(i, rations_choices[i]) for i in range(6)]
    if form.validate_on_submit():
        current_user.county.tax = form.tax.data
        current_user.county.rations = form.rations.data
        db.session.commit()
        return redirect(url_for('economy'))
    return render_template('gameplay/economy.html', form=form)
