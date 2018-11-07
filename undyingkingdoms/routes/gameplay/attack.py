from flask import render_template, url_for, redirect
from flask_login import login_required, current_user

from undyingkingdoms import app, db
from undyingkingdoms.models import County
from undyingkingdoms.models.forms.attack import AttackForm
from undyingkingdoms.static.metadata import all_armies


@login_required
@app.route('/gameplay/attack/<int:county_id>/', methods=['GET', 'POST'])
def attack(county_id):
    enemy = County.query.filter_by(id=county_id).first()
    form = AttackForm()
    if form.validate_on_submit():
        army = {}
        for name, amount, cost, maintenance, description in all_armies:
            if form.data[name] > 0:
                army[name] = form.data[name]
        results = current_user.county.battle_results(army, enemy)
        db.session.commit()
        return render_template('gameplay/attack_results.html', results=results)
    return render_template('gameplay/attack.html', enemy=enemy, results="None", form=form)
