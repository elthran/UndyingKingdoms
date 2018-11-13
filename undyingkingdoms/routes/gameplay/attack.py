from flask import render_template
from flask_login import login_required, current_user

from undyingkingdoms import app, db
from undyingkingdoms.models import County
from undyingkingdoms.models.forms.military import MilitaryForm


@login_required
@app.route('/gameplay/attack/<int:county_id>/', methods=['GET', 'POST'])
def attack(county_id):
    enemy = County.query.filter_by(id=county_id).first()
    form = MilitaryForm()
    if form.validate_on_submit():
        army = {}
        for unit in current_user.county.armies.values():
            if unit.amount < form.data[unit.base]:
                print("You don't have enough troops.")
                return render_template('gameplay/attack.html', enemy=enemy, results="None", form=form)
            army[unit.base] = form.data[unit.base]
        results = current_user.county.battle_results(army, enemy)
        db.session.commit()
        return render_template('gameplay/attack_results.html', results=results)
    return render_template('gameplay/attack.html', enemy=enemy, results="None", form=form)
