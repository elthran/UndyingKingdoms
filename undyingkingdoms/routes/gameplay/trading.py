from flask import render_template, jsonify, request, url_for, redirect
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from undyingkingdoms import app
from undyingkingdoms.models.exports import County, Notification
from undyingkingdoms.models.exports import Trade
from undyingkingdoms.models.forms.trade import TradeForm


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


@app.route('/gameplay/trade/<int:county_id>/', methods=['POST'])
@login_required
def trade(county_id):
    county = current_user.county
    target_county = County.query.get(county_id)

    trade_form = TradeForm()

    trade_form.offer_gold.choices = [(i * 10, i * 10) for i in range(county.gold // 10 + 1)]
    trade_form.offer_wood.choices = [(i * 10, i * 10) for i in range(county.wood // 10 + 1)]
    trade_form.offer_iron.choices = [(i * 10, i * 10) for i in range(county.iron // 10 + 1)]
    trade_form.offer_stone.choices = [(i * 10, i * 10) for i in range(county.stone // 10 + 1)]
    trade_form.offer_grain.choices = [(i * 10, i * 10) for i in range(county.grain_stores // 10 + 1)]

    trade_form.receive_gold.choices = [(i * 10, i * 10) for i in range(51)]
    trade_form.receive_wood.choices = [(i * 10, i * 10) for i in range(51)]
    trade_form.receive_iron.choices = [(i * 10, i * 10) for i in range(51)]
    trade_form.receive_stone.choices = [(i * 10, i * 10) for i in range(51)]
    trade_form.receive_grain.choices = [(i * 10, i * 10) for i in range(51)]
    trade_form.duration.choices = [(i, i) for i in range(12, 25)]

    if trade_form.validate_on_submit() and county != target_county:
        # Consider just passing in the form object.
        trade_offered = Trade(
            county.id,
            target_county.id,
            current_user.county.kingdom.world.day,
            trade_form.duration.data,
            trade_form.offer_gold.data,
            trade_form.offer_wood.data,
            trade_form.offer_iron.data,
            trade_form.offer_stone.data,
            trade_form.offer_grain.data,
            trade_form.receive_gold.data,
            trade_form.receive_wood.data,
            trade_form.receive_iron.data,
            trade_form.receive_stone.data,
            trade_form.receive_grain.data
        )
        trade_offered.save()

        county.gold -= trade_form.offer_gold.data
        county.wood -= trade_form.offer_wood.data
        county.iron -= trade_form.offer_iron.data
        county.stone -= trade_form.offer_stone.data
        county.grain_stores -= trade_form.offer_grain.data

        trade_notice = Notification(
            target_county.id,
            "You were offered a trade",
            f"{county.name} has offered you a trade. Visit the trading page.",
            county.kingdom.world.day,
            "Trade")
        trade_notice.save()

        return redirect(url_for('trading'))

    return jsonify(
        status='fail',
        message="Your trade didn't pass form validation."
    )
