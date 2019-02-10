from datetime import datetime

from flask import render_template, url_for, redirect, request
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from undyingkingdoms import app
from undyingkingdoms.models import County, Kingdom, Message
from undyingkingdoms.models.forms.message import MessageForm
from undyingkingdoms.models.forms.trade import TradeForm
from undyingkingdoms.routes.helpers import in_active_session


@app.route('/gameplay/overview/<int:kingdom_id>/<int:county_id>/', methods=['GET', 'POST'])
@mobile_template('{mobile/}gameplay/overview.html')
@login_required
@in_active_session
def overview(template, kingdom_id=0, county_id=0):
    if not current_user.county:
        return redirect(url_for('initialize'))
    if (kingdom_id == current_user.county.kingdom_id and county_id == current_user.county.id) or (kingdom_id == 0 or county_id == 0):
        has_mail = Message.query.filter_by(county_id=current_user.county.id, unread=True).count()
        return render_template(template, has_mail=has_mail)

    # Would like to move to a POST view.
    message_form = MessageForm()
    if request.args.get('id') == 'message' and message_form.validate_on_submit():
        message = Message(county_id=county_id,
                          title=message_form.title.data,
                          content=message_form.content.data,
                          author_county_id=current_user.county.id,
                          day=current_user.county.kingdom.world.day)
        message.save()
        return redirect(url_for('overview', kingdom_id=kingdom_id, county_id=county_id))

    trade_form = TradeForm()
    if request.args.get('id') == 'trade' and trade_form.validate_on_submit():
        print("Trading:", trade_form)
        return redirect(url_for('overview', kingdom_id=kingdom_id, county_id=county_id))

    target_kingdom = Kingdom.query.filter_by(id=kingdom_id).first()
    target_county = County.query.filter_by(id=county_id).first()

    # Would like to move to a view_enemy route of some kind.
    # Ugly hack to return '{mobile/}gameplay/overview_enemy.html'
    template = '_enemy.'.join(template.split('.'))
    return render_template(template, target_kingdom=target_kingdom, target_county=target_county, message_form=message_form, trade_form=trade_form)
