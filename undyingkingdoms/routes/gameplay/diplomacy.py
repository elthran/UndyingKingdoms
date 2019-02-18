from flask import render_template, jsonify, request, url_for, redirect
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from undyingkingdoms import app
from undyingkingdoms.models import County
from undyingkingdoms.models.trades import Trade


@app.route('/gameplay/diplomacy/', methods=['GET'])
@mobile_template("{mobile/}gameplay/diplomacy.html")
@login_required
def diplomacy(template):
    county = current_user.county
    trades_offered = Trade.query.filter_by(county_id=county.id).filter(Trade.duration > 0).all()
    trades_received = Trade.query.filter_by(target_id=county.id).filter(Trade.duration > 0).all()
    return render_template(template, trades_offered=trades_offered, trades_received=trades_received)


@app.route('/gameplay/diplomacy/<int:trade_id>', methods=['GET'])
@login_required
def diplomacy_reply(trade_id):
    trade = Trade.query.get(trade_id)
    county = County.query.get(trade.county_id)
    target_county = current_user.county  # This will be the current user
    if "accept" in request.args:
        if target_county.gold >= trade.gold_to_receive and target_county.wood >= trade.wood_to_receive and target_county.iron >= trade.iron_to_receive and target_county.stone >= trade.stone_to_receive and target_county.grain_stores >= trade.grain_to_receive:
            target_county.gold += trade.gold_to_give
            target_county.gold -= trade.gold_to_receive
            county.gold += trade.gold_to_receive
            target_county.wood += trade.wood_to_give
            target_county.wood -= trade.wood_to_receive
            county.wood += trade.wood_to_receive
            target_county.iron += trade.iron_to_give
            target_county.iron -= trade.iron_to_receive
            county.iron += trade.iron_to_receive
            target_county.stone += trade.stone_to_give
            target_county.stone -= trade.stone_to_receive
            county.stone += trade.stone_to_receive
            target_county.grain_stores += trade.grain_to_give
            target_county.grain_stores -= trade.grain_to_receive
            county.grain_stores += trade.grain_to_receive
            trade.status = "Accepted"
            return jsonify(
                status='success',
                message='Trade was accepted.'
            ), 200
        else:
            return jsonify(
                status="success",
                message=f"You do not have the resources to accept this trade."
            )
    elif "reject" in request.args:
        trade.status = "Rejected"
        return jsonify(
            status="success",
            message=f"You rejected a trade from {trade_id}"
        )
    elif "cancel" in request.args:
        trade.status = "Cancelled"
        county.gold += trade.gold_to_give
        county.wood += trade.wood_to_give
        county.iron += trade.iron_to_give
        county.stone += trade.stone_to_give
        county.grain += trade.grain_to_give
        return jsonify(
            status="success",
            message=f"You cancelled a trade to {trade_id}"
        )
    return jsonify(
        status="fail",
        message="You sent some malformed data."
    )
