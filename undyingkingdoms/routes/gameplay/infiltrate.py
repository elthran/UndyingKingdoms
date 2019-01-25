from random import randint, choice

from flask import redirect, url_for, render_template
from flask_login import login_required, current_user

from undyingkingdoms import app
from undyingkingdoms.models import Infiltration, County
from undyingkingdoms.models.forms.infiltrate import InfiltrateForm
from undyingkingdoms.static.metadata import infiltration_missions, all_buildings


@app.route('/gameplay/infiltrate/<int:county_id>', methods=['GET', 'POST'])
@login_required
def infiltrate(county_id):
    if not current_user.in_active_session:
        current_user.in_active_session = True
    if county_id == current_user.county.id:
        return redirect(url_for('overview', kingdom_id=0, county_id=0))

    target = County.query.filter_by(id=county_id).first()

    form = InfiltrateForm()
    form.county_id.data = current_user.county.id
    thieves = current_user.county.get_number_of_available_thieves()
    form.amount.choices = [(i+1, i+1) for i in range(thieves)]
    form.mission.choices = [(index, name) for index, name in enumerate(infiltration_missions)]

    if form.validate_on_submit():

        mission = infiltration_missions[form.mission.data]
        report = Infiltration(current_user.county.id, target.id, current_user.county.county_days_in_age,
                              current_user.county.kingdom.world.day,
                              mission, form.amount.data)
        report.save()

        chance_of_success = 100 - (target.get_number_of_available_thieves() * 2000 / target.land)

        if chance_of_success >= randint(1, 100):
            report.success = True
            if mission == 'pilfer':
                gold_stolen = min(randint(15, 25) * form.amount.data, target.gold)
                target.gold -= gold_stolen
                current_user.county.gold += gold_stolen
                report.pilfer_amount = gold_stolen
                report.duration = 14
            elif mission == 'burn crops':
                crops_burned = min(target.buildings['fields'].total, form.amount.data)
                target.buildings['fields'].total -= crops_burned
                report.crops_burned = crops_burned
            elif mission == 'sow distrust':
                happiness_lost = min(target.happiness, form.amount.data * 3)
                target.happiness -= happiness_lost
                report.distrust = happiness_lost
                report.duration = 18
            elif mission == 'scout military':
                report.get_troop_report(current_user.county, target, form.amount.data)
                report.duration = 6
        else:
            report.success = False

        return redirect(url_for('infiltration'))

    return render_template('gameplay/infiltrate.html', target=target, form=form)
