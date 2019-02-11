from datetime import datetime

from flask import render_template, url_for, redirect, request, jsonify
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from undyingkingdoms import app
from undyingkingdoms.models import County, Kingdom, Message
from undyingkingdoms.models.bases import GameState
from undyingkingdoms.models.forms.message import MessageForm
from undyingkingdoms.models.forms.trade import TradeForm
from undyingkingdoms.routes.helpers import in_active_session

"""
Each of these routes could go in their own file

The main concept is that you are separating each concept into
its own route. Even though this cause duplication of code it is much
easeir to test and debug. If you use a major concept in 2 places
you can make that a 'utility' function and import it into both routes.
"""

@app.route('/gameplay/overview', methods=['GET'])
@mobile_template('{mobile/}gameplay/overview.html')
@login_required
@in_active_session
def overview(template):
    # If game has been reset allow user to make a new county.
    if not current_user.county:
        return redirect(url_for('initialize'))

    has_mail = Message.query.filter_by(county_id=current_user.county.id, unread=True).count()
    return render_template(template, has_mail=has_mail)


@app.route('/gameplay/enemy_overview/<int:kingdom_id>/<int:county_id>/', methods=['GET'])
@mobile_template('{mobile/}gameplay/enemy_overview.html')
@login_required
@in_active_session
def enemy_overview(template, kingdom_id=0, county_id=0):
    message_form = MessageForm()
    trade_form = TradeForm()
    target_kingdom = Kingdom.query.filter_by(id=kingdom_id).first()
    target_county = County.query.filter_by(id=county_id).first()
    # import pdb;pdb.set_trace()

    return render_template(template, target_kingdom=target_kingdom, target_county=target_county, message_form=message_form, trade_form=trade_form)


@app.route('/gameplay/send_message/<int:county_id>/', methods=['POST'])
@login_required
@in_active_session
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
        return jsonify(dict(
            status='success',
            message=f'You sent a message to {county_id}'
        ))
    return jsonify(dict(
        status='fail',
        message="Your message didn't pass form validation."
    ))

# move to proper model file
class Trade(GameState):
    def __init__(self, kingdom_id, county_id):
        pass


@app.route('/gameplay/trade/<int:county_id>/', methods=['POST'])
@login_required
@in_active_session
def trade(county_id):

    county = County.query.get(county_id)
    kingdom_id = county.kingdom_id

    trade_form = TradeForm()
    if trade_form.validate_on_submit():
        trade = Trade(kingdom_id, county_id)

        trade.save()
        return jsonify(dict(
            status='success',
            message=f'You sent a trade to {county_id}'
        ))
    return jsonify(dict(
        status='fail',
        message="Your trade didn't pass form validation."
    ))

