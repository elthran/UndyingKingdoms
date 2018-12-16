from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from undyingkingdoms import app, db
from undyingkingdoms.models import World, Transaction
from undyingkingdoms.models.forms.infrastructure import InfrastructureForm
from undyingkingdoms.static.metadata import all_buildings, game_descriptions


@login_required
@app.route('/gameplay/infrastructure/', methods=['GET', 'POST'])
def infrastructure():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    county = current_user.county
    world = World.query.filter_by(id=county.kingdom.world_id).first()
    form = InfrastructureForm()
    form.county_id.data = county.id
    if form.validate_on_submit():
        transaction = Transaction(current_user.id, world.day, "buy", county.gold, county.wood, county.iron)
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
        db.session.add(transaction)
        db.session.commit()
        return redirect(url_for('infrastructure'))
    else:
        print(form.data)
    return render_template('gameplay/infrastructure.html', form=form, meta_data=game_descriptions)

