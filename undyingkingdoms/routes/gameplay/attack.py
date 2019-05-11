from flask import render_template
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from undyingkingdoms import app
from undyingkingdoms.models.exports import County
from undyingkingdoms.models.forms.attack import AttackForm
from undyingkingdoms.routes.helpers import not_self, not_allies
from undyingkingdoms.metadata.metadata import attack_types


@app.route('/gameplay/attack/<int:county_id>/', methods=['GET', 'POST'])
@mobile_template('{mobile/}gameplay/attack.html')
@not_self
@not_allies
@login_required
def attack(template, county_id):
    county = current_user.county
    kingdom = county.kingdom
    enemy = County.query.get(county_id)
    enemy_kingdom = enemy.kingdom

    # This war code is just so the HTML knows if you are at war for points....
    war = kingdom.at_war_with(enemy_kingdom)

    form = AttackForm(county)

    unit_types = (_type for _type in county.armies if _type not in 'archer')

    for key in unit_types:
        field = getattr(form, key)
        troops = county.armies[key].available
        if troops < 10:
            field.choices = [(i, i) for i in range(troops + 1)]
        else:
            field.choices = [(troops * i // 10, troops * i // 10) for i in range(0, 11)]

    form.attack_type.choices = [(_type, _type) for _type in attack_types]

    if form.validate_on_submit():
        results = county.battle_results(form.army, enemy, form.attack_type.data)

        # Would like to move to a attack_results route of some kind.
        # Ugly hack to return '{mobile/}gameplay/attack_results.html'
        template = '_results.'.join(template.split('.'))
        return render_template(template, results=results)
    return render_template(template, enemy=enemy, form=form, war=war)
