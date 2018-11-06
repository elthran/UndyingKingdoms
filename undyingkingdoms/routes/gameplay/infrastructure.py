from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from undyingkingdoms import app, db
from undyingkingdoms.models.forms.infrastructure import InfrastructureForm
from undyingkingdoms.static.metadata import all_buildings


@login_required
@app.route('/gameplay/infrastructure/', methods=['GET', 'POST'])
def infrastructure():
    form = InfrastructureForm()
    if form.validate_on_submit():
        # This needs to not validate if the sum(data) in the form exceeds available land
        for name, amount, cost, maintenance, description in all_buildings:
            if form.data[name] > 0:
                current_user.county.buildings[name].pending += form.data[name]
        db.session.commit()
        return redirect(url_for('infrastructure'))
    return render_template('gameplay/infrastructure.html', form=form)

