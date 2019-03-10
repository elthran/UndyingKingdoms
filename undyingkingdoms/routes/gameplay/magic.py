from flask import render_template, url_for
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template
from werkzeug.utils import redirect

from undyingkingdoms import app
from undyingkingdoms.models.magic import Magic
from undyingkingdoms.models.spells import Spell


@app.route('/gameplay/magic/', methods=['GET', 'POST'])
@mobile_template("{mobile/}gameplay/magic.html")
@login_required
def magic(template):
    known_spells = Magic.query.filter_by(county_id=current_user.county.id).filter_by(known=True).all()
    unknown_spells = Magic.query.filter_by(county_id=current_user.county.id).filter_by(known=False).all()
    active_spells = Spell.query.filter_by(county_id=current_user.county.id).filter((Spell.duration > 0) | (Spell.active==True)).all()
    casting_history = Spell.query.filter_by(county_id=current_user.county.id).all()
    sustain_mana_requirement = sum(spell.mana_sustain for spell in active_spells)
    return render_template(template,
                           known_spells=known_spells,
                           unknown_spells=unknown_spells,
                           active_spells=active_spells,
                           casting_history=casting_history,
                           sustain_mana_requirement=sustain_mana_requirement)


@app.route('/gameplay/cast_spell/<int:spell_id>', methods=['GET', 'POST'])
@login_required
def cast_spell(spell_id):
    county = current_user.county
    spell = Magic.query.get(spell_id)
    if spell is None or spell.mana_cost > county.mana:
        return redirect(url_for('magic'))
    county.mana -= spell.mana_cost
    print("mana sustain..", spell.mana_sustain)

    cast = Spell(county.id, 0, county.kingdom.world.day, county.day, spell.name)
    cast.save()
    if spell.mana_sustain > 0:
        cast.active = True
        cast.mana_sustain = spell.mana_sustain

    if cast.name == 'inspire':
        county.happiness += 5
    elif cast.name == 'summon golem':
        pass
    elif cast.name == 'plague winds':
        pass
    return redirect(url_for('magic'))
