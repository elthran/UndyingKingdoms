from flask import render_template
from flask_login import login_required, current_user

from undyingkingdoms import app, db
from undyingkingdoms.models import County
from undyingkingdoms.models.forms.attack import AttackForm
from undyingkingdoms.models.forms.military import MilitaryForm


@login_required
@app.route('/gameplay/attack/<int:county_id>/', methods=['GET', 'POST'])
def attack(county_id):
    enemy = County.query.filter_by(id=county_id).first()
    form = AttackForm()

    peasants = sum([army.amount for army in current_user.county.armies.values() if army.base == 'peasant'])
    archer = sum([army.amount for army in current_user.county.armies.values() if army.base == 'archer'])
    soldier = sum([army.amount for army in current_user.county.armies.values() if army.base == 'soldier'])
    elite = sum([army.amount for army in current_user.county.armies.values() if army.base == 'elite'])
    print(peasants, archer, soldier, elite)

    form.peasant.choices = [(amount, amount) for amount in range(peasants)]
    form.archer.choices = [(amount, amount) for amount in range(archer)]
    form.soldier.choices = [(amount, amount) for amount in range(soldier)]
    form.elite.choices = [(amount, amount) for amount in range(elite)]
    print(form.peasant.choices, form.archer.choices, form.soldier.choices, form.elite.choices)

    if not form.peasant.choices:
        form.peasant.choices = [(0, 0)]
    if not form.archer.choices:
        form.archer.choices = [(0, 0)]
    if not form.soldier.choices:
        form.soldier.choices = [(0, 0)]
    if not form.elite.choices:
        form.elite.choices = [(0, 0)]

    if form.validate_on_submit():
        print("validated")
        army = {}
        for unit in current_user.county.armies.values():
            if unit.amount < form.data[unit.base]:
                return render_template('gameplay/attack.html', enemy=enemy, form=form)
            army[unit.base] = form.data[unit.base]
        results = current_user.county.battle_results(army, enemy)
        db.session.commit()
        return render_template('gameplay/attack_results.html', results=results)
    return render_template('gameplay/attack.html', enemy=enemy, form=form)
