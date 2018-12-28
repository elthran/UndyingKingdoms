from flask import render_template
from flask_login import login_required, current_user

from undyingkingdoms import app, db
from undyingkingdoms.models import County
from undyingkingdoms.models.forms.attack import AttackForm


@app.route('/gameplay/attack/<int:county_id>/', methods=['GET', 'POST'])
@login_required
def attack(county_id):
    if not current_user.logged_in:
        current_user.logged_in = True
    enemy = County.query.filter_by(id=county_id).first()
    form = AttackForm()

    peasants = current_user.county.armies['peasant'].available + 1
    archers = current_user.county.armies['archer'].available + 1
    soldiers = current_user.county.armies['soldier'].available + 1
    elites = current_user.county.armies['elite'].available + 1

    form.peasant.choices = [(amount, amount) for amount in range(peasants)]
    form.archer.choices = [(amount, amount) for amount in range(archers)]
    form.soldier.choices = [(amount, amount) for amount in range(soldiers)]
    form.elite.choices = [(amount, amount) for amount in range(elites)]

    if form.validate_on_submit():
        army = {}
        for unit in current_user.county.armies.values():
            if unit.total < form.data[unit.base_name]:
                return render_template('gameplay/attack.html', enemy=enemy, form=form)
            army[unit.base_name] = form.data[unit.base_name]
        results = current_user.county.battle_results(army, enemy)
        db.session.commit()
        return render_template('gameplay/attack_results.html', results=results)
    return render_template('gameplay/attack.html', enemy=enemy, form=form)
