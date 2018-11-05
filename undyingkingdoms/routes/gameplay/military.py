from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from undyingkingdoms import app, db
from undyingkingdoms.models.forms.military import MilitaryForm
from undyingkingdoms.static.metadata import all_armies


@login_required
@app.route('/gameplay/military', methods=['GET', 'POST'])
def military():
    form = MilitaryForm()
    if form.validate_on_submit():
        for name, amount, attack, defence, health in all_armies:
            if form.data[name] > 0:
                current_user.county.armies[name].pending += form.data[name]
        db.session.commit()
        return redirect(url_for('military'))
    return render_template('gameplay/military.html', form=form)
