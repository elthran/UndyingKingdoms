from flask import render_template, jsonify, request
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template
from sqlalchemy import desc

from undyingkingdoms import app
from undyingkingdoms.models import Infiltration
from undyingkingdoms.models.trades import Trade


@app.route('/gameplay/diplomacy/', methods=['GET'])
@mobile_template("{mobile/}gameplay/diplomacy.html")
@login_required
def diplomacy(template):
    if not current_user.in_active_session:
        current_user.in_active_session = True
    county = current_user.county
    trades_offered = Trade.query.filter_by(county_id=county.id).filter(Trade.duration > 0).all()
    trades_received = Trade.query.filter_by(target_id=county.id).filter(Trade.duration > 0).all()
    return render_template(template, trades_offered=trades_offered, trades_received=trades_received)


@app.route('/gameplay/diplomacy/<int:trade_id>', methods=['GET'])
@login_required
def diplomacy_reply(trade_id):
    print(request.args)

    trade = Trade.query.get(trade_id)

    print(trade)
    if "accept" in request.args:
        # Accept the trade.
        # return whatever data you need to client.
        return jsonify(dict(
            status="success",
            message=f"You accepted a trade from {trade_id}"
        ))
    elif "reject" in request.args:
        # reject the trade
        # return whatever data you need to client.
        return jsonify(dict(
            status="success",
            message=f"You rejected a trade from {trade_id}"
        ))
    # Your is missing something, you should only get here
    # if the trade doesn't exist.
    return jsonify(dict(
        status="fail",
        message="You sent some malformed data."
    ))
