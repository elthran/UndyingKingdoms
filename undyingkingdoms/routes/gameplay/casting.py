from flask import render_template, url_for
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template
from werkzeug.utils import redirect

from undyingkingdoms import app
from undyingkingdoms.models import County, Notification
from undyingkingdoms.models.magic import Magic
from undyingkingdoms.models.casting import Casting


@app.route('/gameplay/casting/<target_id>', methods=['GET', 'POST'])
@mobile_template("{mobile/}gameplay/casting.html")
@login_required
def casting(template, target_id):
    county = current_user.county
    target_county = County.query.get(target_id)
    if target_county == county:
        targets = 'self'
    elif target_county.kingdom in county.kingdom.allies:
        targets = 'friendly'
    elif target_county.kingdom in county.kingdom.enemies:
        targets = 'hostile'
    else:
        targets = 'all'
    known_spells = Magic.get_know_spells(county)
    unknown_spells = Magic.get_unknown_spells(county)
    active_spells = Casting.get_active_spells(county)
    enemy_spells = Casting.get_enemy_spells(county)
    casting_history = Casting.query.filter_by(county_id=county.id).all()
    sustain_mana_requirement = Casting.get_sustain_mana_requirement(county)
    return render_template(
        template,
        target=target_county,
        targets=targets,
        known_spells=known_spells,
        unknown_spells=unknown_spells,
        active_spells=active_spells,
        enemy_spells=enemy_spells,
        casting_history=casting_history,
        sustain_mana_requirement=sustain_mana_requirement
    )


@app.route('/gameplay/cast_spell/<int:spell_id>/<int:target_id>', methods=['GET', 'POST'])
@login_required
def cast_spell(spell_id, target_id):
    county = current_user.county
    target = County.query.get(target_id)
    spell = Magic.query.get(spell_id)

    if county == target:
        target_relation = 'self'
    elif target.kingdom in county.kingdom.allies:
        target_relation = 'friendly'
    else:
        target_relation = 'hostile'

    if (spell is None
            or target is None
            or spell.mana_cost > county.mana
            or target_relation != spell.targets
            or not spell.known):
        return redirect(url_for('casting', target_id=target.id))
    county.mana -= spell.mana_cost

    cast = Casting(county.id, target.id, spell.id, county.kingdom.world.day, county.day, spell.name, spell.duration)
    cast.target_relation = target_relation
    cast.save()

    if spell.mana_sustain > 0:
        cast.active = True
        cast.mana_sustain = spell.mana_sustain

    if cast.name == 'inspire':
        county.happiness += 5
    elif cast.name == 'summon golem':
        pass
    elif cast.name == 'plague winds':
        notification = Notification(
            target.id,
            "Enemy magic", "A plague wind has been summoned by the wizards of {}".format(county.name),
            county.kingdom.world.day,
            "Magic")
        notification.save()
        pass
    return redirect(url_for('casting', target_id=target.id))


@app.route('/gameplay/cancel_spell/<int:spell_id>', methods=['GET', 'POST'])
@login_required
def cancel_spell(spell_id):
    county = current_user.county
    spell = Casting.query.get(spell_id)
    if spell is None or county.id != spell.county_id:
        return redirect(url_for('casting', target_id=county.id))
    spell.active = False
    spell.duration = 0
    return redirect(url_for('casting', target_id=county.id))


@app.route('/gameplay/dispel_spell/<int:spell_id>', methods=['GET', 'POST'])
@login_required
def dispel_spell(spell_id):
    county = current_user.county
    spell = Casting.query.get(spell_id)
    if (spell is None
            or county.mana < 10
            or spell.target_id != county.id):
        return redirect(url_for('casting', target_id=current_user.county.id))
    spell.active = False
    spell.duration = 0
    county.mana -= 10
    return redirect(url_for('casting', target_id=current_user.county.id))
