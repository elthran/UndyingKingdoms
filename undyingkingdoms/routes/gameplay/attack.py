from flask import render_template, url_for, redirect
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from undyingkingdoms import app
from undyingkingdoms.models import County
from undyingkingdoms.models.forms.attack import AttackForm
from undyingkingdoms.routes.helpers import in_active_session


@app.route('/gameplay/attack/<int:county_id>/', methods=['GET', 'POST'])
@mobile_template('{mobile/}gameplay/attack.html')
@login_required
@in_active_session
def attack(template, county_id):
    if county_id == current_user.county.id:
        return redirect(url_for('overview', kingdom_id=0, county_id=0))
    enemy = County.query.filter_by(id=county_id).first()
    form = AttackForm()

    peasant = current_user.county.armies['peasant'].available
    soldier = current_user.county.armies['soldier'].available
    elite = current_user.county.armies['elite'].available
    monster = current_user.county.armies['monster'].available

    if peasant == 0:
        form.peasant.choices = [(0, 0)]
    elif peasant < 10:
        form.peasant.choices = [(i, i) for i in range(peasant + 1)]
    else:
        form.peasant.choices = [(peasant * i // 10, peasant * i // 10) for i in range(0, 11)]
    if soldier == 0:
        form.soldier.choices = [(0, 0)]
    elif soldier < 10:
        form.soldier.choices = [(i, i) for i in range(soldier + 1)]
    else:
        form.soldier.choices = [(soldier * i // 10, soldier * i // 10) for i in range(0, 11)]
    if elite == 0:
        form.elite.choices = [(0, 0)]
    elif elite < 10:
        form.elite.choices = [(i, i) for i in range(0, elite + 1)]
    else:
        form.elite.choices = [(elite * i // 10, elite * i // 10) for i in range(0, 11)]
    if monster == 0:
        form.monster.choices = [(0, 0)]
    elif monster < 10:
        form.monster.choices = [(i, i) for i in range(0, monster + 1)]
    else:
        form.monster.choices = [(monster * i // 10, monster * i // 10) for i in range(0, 11)]

    if form.validate_on_submit():
        army = {}
        for unit in current_user.county.armies.values():
            if unit.base_name != 'archer':
                if unit.total < form.data[unit.base_name]:
                    return render_template(template, enemy=enemy, form=form)
                army[unit.base_name] = form.data[unit.base_name]
        results = current_user.county.battle_results(army, enemy)

        # Would like to move to a attack_results route of some kind.
        # Ugly hack to return '{mobile/}gameplay/attack_results.html'
        template = '_results.'.join(template.split('.'))
        return render_template(template, results=results)
    return render_template(template, enemy=enemy, form=form)
