from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from undyingkingdoms import app, db
from undyingkingdoms.models.forms.infrastructure import InfrastructureForm
from undyingkingdoms.static.metadata import all_buildings


@login_required
@app.route('/gameplay/infrastructure/', methods=['GET', 'POST'])
def infrastructure():
    county = current_user.county
    form = InfrastructureForm()
    form.county_id.data = county.id
    if form.validate_on_submit():
        for building in all_buildings:
            if form.data[building] > 0:
                county.gold -= form.data[building] * county.buildings[building].gold
                county.wood -= form.data[building] * county.buildings[building].wood
                county.buildings[building].pending += form.data[building]
        db.session.commit()
        return redirect(url_for('infrastructure'))
    return render_template('gameplay/infrastructure.html', form=form)

