from flask import render_template, jsonify, request
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from undyingkingdoms import app
from undyingkingdoms.models.exports import County, Notification
from undyingkingdoms.models.exports import Trade


@app.route('/gameplay/trading/', methods=['GET'])
@mobile_template("{mobile/}gameplay/trading.html")
@login_required
def trading(template):
    county = current_user.county
    trades_offered = Trade.query.filter_by(county_id=county.id).filter(Trade.duration > 0).all()
    trades_received = Trade.query.filter_by(target_id=county.id).filter(Trade.duration > 0).all()
    return render_template(template, trades_offered=trades_offered, trades_received=trades_received)


@app.route('/gameplay/trading/<int:trade_id>', methods=['GET'])
@login_required
def trading_reply(trade_id):
    trade = Trade.query.get(trade_id)
    trade_offerer = County.query.get(trade.county_id)
    trade_target = County.query.get(trade.target_id)
    your_county = current_user.county  # This will be the current user
    if ("accept" in request.args and
            trade.status == "Pending" and
            trade_target == your_county):
        if your_county.gold >= trade.gold_to_receive and your_county.wood >= trade.wood_to_receive and your_county.iron >= trade.iron_to_receive and your_county.stone >= trade.stone_to_receive and your_county.grain_stores >= trade.grain_to_receive:
            your_county.gold += trade.gold_to_give
            your_county.gold -= trade.gold_to_receive
            trade_offerer.gold += trade.gold_to_receive
            your_county.wood += trade.wood_to_give
            your_county.wood -= trade.wood_to_receive
            trade_offerer.wood += trade.wood_to_receive
            your_county.iron += trade.iron_to_give
            your_county.iron -= trade.iron_to_receive
            trade_offerer.iron += trade.iron_to_receive
            your_county.stone += trade.stone_to_give
            your_county.stone -= trade.stone_to_receive
            trade_offerer.stone += trade.stone_to_receive
            your_county.grain_stores += trade.grain_to_give
            your_county.grain_stores -= trade.grain_to_receive
            trade_offerer.grain_stores += trade.grain_to_receive
            trade.status = "Accepted"
            notice = Notification(trade_offerer.id, "Trade", f"Your trade was accepted by {current_user.county.name}",
                                  current_user.county.kingdom.world.day, category="Trade")
            notice.save()
            return jsonify(
                status='success',
                message='Trade was accepted.'
            ), 200
        else:
            return jsonify(
                status="fail",
                message=f"You do not have the resources to accept this trade."
            )
    elif "reject" in request.args and trade_target == your_county:
        trade.status = "Rejected"
        notice = Notification(trade_offerer.id, "Trade", f"Your trade was rejected by {current_user.county.name}",
                              current_user.county.kingdom.world.day, category="Trade")
        notice.save()
        return jsonify(
            status="success",
            message=f"You rejected a trade from {trade_id}"
        )
    elif ("cancel" in request.args and
          trade.status == "Pending" and
          trade_offerer == your_county):
        trade.status = "Cancelled"
        trade_offerer.gold += trade.gold_to_give
        trade_offerer.wood += trade.wood_to_give
        trade_offerer.iron += trade.iron_to_give
        trade_offerer.stone += trade.stone_to_give
        trade_offerer.grain_stores += trade.grain_to_give
        return jsonify(
            status="success",
            message=f"You cancelled a trade to {trade_id}"
        )
    return jsonify(
        status="fail",
        message="You sent some malformed data."
    )
