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
    target_county = County.query.get(target_id)
    if target_county == current_user.county:
        targets = 'self'
    elif target_county.kingdom in current_user.county.kingdom.allies:
        targets = 'friendly'
    elif target_county.kingdom in current_user.county.kingdom.enemies:
        targets = 'hostile'
    else:
        targets = 'all'
    known_spells = Magic.query.filter_by(county_id=current_user.county.id).filter_by(known=True).all()
    unknown_spells = Magic.query.filter_by(county_id=current_user.county.id).filter_by(known=False).all()
    active_spells = Casting.query.filter_by(county_id=current_user.county.id).filter((Casting.duration > 0) | (Casting.active==True)).all()
    enemy_spells = Casting.query.filter_by(target_id=current_user.county.id).filter((Casting.duration > 0) | (Casting.active==True)).all()
    casting_history = Casting.query.filter_by(county_id=current_user.county.id).all()
    sustain_mana_requirement = sum(spell.mana_sustain for spell in active_spells)
    return render_template(template, target=target_county, targets=targets,
                           known_spells=known_spells,
                           unknown_spells=unknown_spells,
                           active_spells=active_spells,
                           enemy_spells=enemy_spells,
                           casting_history=casting_history,
                           sustain_mana_requirement=sustain_mana_requirement)


@app.route('/gameplay/cast_spell/<int:spell_id>/<int:target_id>', methods=['GET', 'POST'])
@login_required
def cast_spell(spell_id, target_id):
    county = current_user.county
    target = County.query.get(target_id)
    spell = Magic.query.get(spell_id)
    if spell is None or target is None or spell.mana_cost > county.mana:
        return redirect(url_for('casting', target_id=target.id))
    county.mana -= spell.mana_cost

    cast = Casting(county.id, target.id, county.kingdom.world.day, county.day, spell.name, spell.duration)
    cast.save()
    if spell.mana_sustain > 0:
        cast.active = True
        cast.mana_sustain = spell.mana_sustain

    if cast.name == 'inspire':
        county.happiness += 5
    elif cast.name == 'summon golem':
        pass
    elif cast.name == 'plague winds':
        notification = Notification(target.id,
                                    "Enemy magic", "A plague wind has been summoned by the wizards of {}".format(county.name),
                                    county.kingdom.world.day,
                                    "Magic")
        notification.save()
        pass
    return redirect(url_for('casting', target_id=target.id))


@app.route('/gameplay/cancel_spell/<int:spell_id>', methods=['GET', 'POST'])
@login_required
def cancel_spell(spell_id):
    spell = Casting.query.get(spell_id)
    if spell is None:
        return redirect(url_for('casting', target_id=current_user.county.id))
    spell.active = False
    spell.duration = 0
    return redirect(url_for('casting', target_id=current_user.county.id))


@app.route('/gameplay/dispel_spell/<int:spell_id>', methods=['GET', 'POST'])
@login_required
def dispel_spell(spell_id):
    spell = Casting.query.get(spell_id)
    if spell is None:
        return redirect(url_for('casting', target_id=current_user.county.id))
    spell.active = False
    spell.duration = 0
    return redirect(url_for('casting', target_id=current_user.county.id))
