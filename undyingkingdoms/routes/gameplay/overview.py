from datetime import datetime

from flask import render_template, url_for, redirect, request, jsonify
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from undyingkingdoms import app
from undyingkingdoms.blueprints.api.views.helpers import patch_has_mail
from undyingkingdoms.models import County, Kingdom, Message, Notification
from undyingkingdoms.models.bases import GameState
from undyingkingdoms.models.forms.message import MessageForm
from undyingkingdoms.models.forms.trade import TradeForm
from undyingkingdoms.models.trades import Trade

"""
Each of these routes could go in their own file

The main concept is that you are separating each concept into
its own route. Even though this cause duplication of code it is much
easier to test and debug. If you use a major concept in 2 places
you can make that a 'utility' function and import it into both routes.

The Routes that return JSON could be made to return a redirect to 
the overview or overiew_enemy pages but JSON is easier to handle with
JS ... You would need a JS function to submit you form and handle the
callback. The callback would update any relvant data on the page
on the success of the Trade or Send Message routes. 

The Trade and Send Message routes might need to return more data 
than they currently are.
"""


@app.route('/gameplay/overview', methods=['GET'])
@mobile_template('{mobile/}gameplay/overview.html')
@login_required
def overview(template):
    # If game has been reset allow user to make a new county.
    if not current_user.county:
        return redirect(url_for('initialize'))
    patch_has_mail(current_user)

    return render_template(template, has_mail=current_user.has_mail())


@app.route('/gameplay/enemy_overview/<int:kingdom_id>/<int:county_id>/', methods=['GET'])
@mobile_template('{mobile/}gameplay/enemy_overview.html')
@login_required
def enemy_overview(template, kingdom_id=0, county_id=0):
    county = current_user.county
    target_county = County.query.filter_by(id=county_id).first()
    target_kingdom = Kingdom.query.filter_by(id=kingdom_id).first()

    message_form = MessageForm()
    trade_form = TradeForm()

    # should be able to be moved to form init? And just
    # accept gold, wood and iron?
    trade_form.offer_gold.choices = [(i * 10, i * 10) for i in range(county.gold // 10 + 1)]
    trade_form.offer_wood.choices = [(i * 10, i * 10) for i in range(county.wood // 10 + 1)]
    trade_form.offer_iron.choices = [(i * 10, i * 10) for i in range(county.iron // 10 + 1)]
    trade_form.offer_stone.choices = [(i * 10, i * 10) for i in range(county.stone // 10 + 1)]
    trade_form.receive_gold.choices = [(i * 10, i * 10) for i in range(51)]
    trade_form.receive_wood.choices = [(i * 10, i * 10) for i in range(51)]
    trade_form.receive_iron.choices = [(i * 10, i * 10) for i in range(51)]
    trade_form.receive_stone.choices = [(i * 10, i * 10) for i in range(51)]
    trade_form.duration.choices = [(i, i) for i in range(3, 25)]

    return render_template(
        template,
        target_county=target_county,
        target_kingdom=target_kingdom,
        message_form=message_form,
        trade_form=trade_form
    )


@app.route('/gameplay/send_message/<int:county_id>/', methods=['POST'])
@login_required
def send_message(county_id):
    message_form = MessageForm()
    if message_form.validate_on_submit():
        message = Message(
            county_id=county_id,
            title=message_form.title.data,
            content=message_form.content.data,
            author_county_id=current_user.county.id,
            day=current_user.county.kingdom.world.day)
        message.save()
        return jsonify(
            status='success',
            message=f'You sent a message to {county_id}'
        )
    return jsonify(
        status='fail',
        message="Your message didn't pass form validation."
    )


@app.route('/gameplay/trade/<int:county_id>/', methods=['POST'])
@login_required
def trade(county_id):
    county = current_user.county
    target_county = County.query.get(county_id)
    kingdom_id = county.kingdom_id

    trade_form = TradeForm()

    trade_form.offer_gold.choices = [(i * 10, i * 10) for i in range(county.gold // 10 + 1)]
    trade_form.offer_wood.choices = [(i * 10, i * 10) for i in range(county.wood // 10 + 1)]
    trade_form.offer_iron.choices = [(i * 10, i * 10) for i in range(county.iron // 10 + 1)]
    trade_form.offer_stone.choices = [(i * 10, i * 10) for i in range(county.stone // 10 + 1)]
    trade_form.receive_gold.choices = [(i * 10, i * 10) for i in range(51)]
    trade_form.receive_wood.choices = [(i * 10, i * 10) for i in range(51)]
    trade_form.receive_iron.choices = [(i * 10, i * 10) for i in range(51)]
    trade_form.receive_stone.choices = [(i * 10, i * 10) for i in range(51)]
    trade_form.duration.choices = [(i, i) for i in range(3, 25)]

    if trade_form.validate_on_submit():
        trade_offered = Trade(county.id, target_county.id, current_user.county.kingdom.world.day, 12,
                              trade_form.offer_gold.data, trade_form.offer_wood.data, trade_form.offer_iron.data, trade_form.offer_stone.data,
                              trade_form.receive_gold.data, trade_form.receive_wood.data, trade_form.receive_iron.data, trade_form.receive_stone.data)
        trade_offered.save()

        county.gold -= trade_form.offer_gold.data
        county.wood -= trade_form.offer_wood.data
        county.iron -= trade_form.offer_iron.data
        county.stone -= trade_form.offer_stone.data

        trade_notice = Notification(target_county.id, "You were offered a trade",
                                    "{} has offered you a trade. Visit the diplomacy page.".format(county.name),
                                    county.kingdom.world.day)
        trade_notice.save()

        return redirect(url_for('diplomacy'))

    return jsonify(
        status='fail',
        message="Your trade didn't pass form validation."
    )
