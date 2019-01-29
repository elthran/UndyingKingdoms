from flask import render_template, url_for, redirect
from flask_login import login_required, current_user

from undyingkingdoms import app
from undyingkingdoms.models import County
from undyingkingdoms.models.forms.attack import AttackForm


@app.route('/gameplay/attack/<int:county_id>/', methods=['GET', 'POST'])
@login_required
def attack(county_id):
    if not current_user.in_active_session:
        current_user.in_active_session = True
    if county_id == current_user.county.id:
        return redirect(url_for('overview', kingdom_id=0, county_id=0))
    enemy = County.query.filter_by(id=county_id).first()
    form = AttackForm()

    peasants = current_user.county.armies['peasant'].available
    soldiers = current_user.county.armies['soldier'].available
    elites = current_user.county.armies['elite'].available

    if peasants == 0:
        form.peasant.choices = [(0, 0)]
    elif peasants < 10:
        form.peasant.choices = [(i, i) for i in range(peasants)]
    else:
        form.peasant.choices = [(peasants * i // 10, peasants * i // 10) for i in range(0, 11)]
    if soldiers == 0:
        form.soldier.choices = [(0, 0)]
    elif soldiers < 10:
        form.soldier.choices = [(i, i) for i in range(soldiers)]
    else:
        form.soldier.choices = [(soldiers * i // 10, soldiers * i // 10) for i in range(0, 11)]
    if elites == 0:
        form.elite.choices = [(0, 0)]
    elif elites < 10:
        form.elite.choices = [(i, i) for i in range(0, elites + 1)]
    else:
        form.elite.choices = [(elites * i // 10, elites * i // 10) for i in range(0, 11)]

    if form.validate_on_submit():
        army = {}
        for unit in current_user.county.armies.values():
            if unit.base_name != 'archer':
                if unit.total < form.data[unit.base_name]:
                    return render_template('gameplay/attack.html', enemy=enemy, form=form)
                army[unit.base_name] = form.data[unit.base_name]
        results = current_user.county.battle_results(army, enemy)
        return render_template('gameplay/attack_results.html', results=results)
    return render_template('gameplay/attack.html', enemy=enemy, form=form)
