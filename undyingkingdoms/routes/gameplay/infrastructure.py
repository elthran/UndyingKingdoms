from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from undyingkingdoms import app
from undyingkingdoms.models import World, Transaction
from undyingkingdoms.models.forms.infrastructure import InfrastructureForm
from undyingkingdoms.static.metadata import all_buildings, game_descriptions


@app.route('/gameplay/infrastructure/', methods=['GET', 'POST'])
@mobile_template('{mobile/}gameplay/infrastructure.html')
@login_required
def infrastructure(template):
    if not current_user.in_active_session:
        current_user.in_active_session = True
    county = current_user.county
    world = World.query.filter_by(id=county.kingdom.world_id).first()
    form = InfrastructureForm()
    form.county_id.data = county.id
    if form.validate_on_submit():
        transaction = Transaction(county.id, county.county_days_in_age, world.day, "buy")
        for building in all_buildings:
            if form.data[building] > 0:
                county.gold -= form.data[building] * county.buildings[building].gold
                county.wood -= form.data[building] * county.buildings[building].wood
                county.buildings[building].pending += form.data[building]
                transaction.add_purchase(item_name=building,
                                         item_amount=form.data[building],
                                         gold_per_item=county.buildings[building].gold,
                                         wood_per_item=county.buildings[building].wood,
                                         iron_per_item=0)
        transaction.save()
        return redirect(url_for('infrastructure'))
    return render_template(template, form=form, meta_data=game_descriptions)

