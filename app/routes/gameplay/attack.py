from importlib import import_module

from flask import render_template
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from app import app
get_models = lambda: import_module('app.models.exports')
get_forms = lambda: import_module('app.models.forms.exports')
from app.routes.helpers import not_self, neither_allies_nor_armistices
from app.metadata.metadata import attack_types


@app.route('/gameplay/attack/<int:county_id>/', methods=['GET', 'POST'])
@mobile_template('{mobile/}gameplay/attack.html')
@not_self
@neither_allies_nor_armistices
@login_required
def attack(template, county_id):
    models = get_models()
    forms = get_forms()
    county = current_user.county
    kingdom = county.kingdom
    enemy = models.County.query.get(county_id)
    enemy_kingdom = enemy.kingdom

    # This war code is just so the HTML knows if you are at war for points....
    war = kingdom.at_war_with(enemy_kingdom)

    form = forms.AttackForm(county)

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
        results, offence_damage = county.battle_results(form.army, enemy, form.attack_type.data)

        # Would like to move to a attack_results route of some kind.
        # Ugly hack to return '{mobile/}gameplay/attack_results.html'
        template = '_results.'.join(template.split('.'))
        return render_template(template, results=results, offence_damage=offence_damage)
    return render_template(template, enemy=enemy, form=form, war=war)
