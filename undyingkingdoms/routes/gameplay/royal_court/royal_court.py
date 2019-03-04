from flask import redirect, url_for, render_template
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from undyingkingdoms import app
from undyingkingdoms.models import Diplomacy
from undyingkingdoms.models.forms.royal_court import RoyalCourtMessageForm
from undyingkingdoms.routes.gameplay.royal_court.helpers import build_relations_form


@app.route('/gameplay/royal_court/', methods=['GET', 'POST'])
@mobile_template('{mobile/}gameplay/royal_court.html')
@login_required
def royal_court(template):
    county = current_user.county
    kingdom = county.kingdom

    if county.id != county.kingdom.leader:
        return redirect(url_for('overview', kingdom_id=0, county_id=0))
    message_form = RoyalCourtMessageForm()

    relations_form = build_relations_form(county.kingdom)

    # enemy_kingdoms = county.kingdom.get_enemies()
    # ally_list = county.kingdom.get_allies()
    # allies = {}
    # for ally in ally_list:
    #     allies[ally.id] = ally
    # alliances = Diplomacy.query.filter_by(status="In Progress").filter_by(action="Alliance") \
    #         .filter((Diplomacy.kingdom_id == county.kingdom.id) | (Diplomacy.target_id == county.kingdom.id)) \
    #         .all()
    # offers_to_us = county.kingdom.get_pending_alliance(keyword="to")
    # offers_from_us = county.kingdom.get_pending_alliance(keyword="from")
    return render_template(
        template,
        message_form=message_form,
        relations_form=relations_form,
        allies=kingdom.allies,
        enemy_kingdoms=kingdom.enemies,
        alliances=kingdom.alliances,
        pending_alliances=kingdom.pending_alliances,
        offers_to_us=kingdom.kingdoms_who_offered_us_alliances,
        offers_from_us=kingdom.kingdoms_who_we_offered_alliances_to
    )
