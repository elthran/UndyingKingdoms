from datetime import datetime

from flask import render_template, url_for, redirect
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from undyingkingdoms import app
from undyingkingdoms.models import County, Kingdom, Message
from undyingkingdoms.models.forms.message import MessageForm
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
    form = MessageForm()
    if form.validate_on_submit():
        message = Message(county_id=county_id,
                          title=form.title.data,
                          content=form.content.data,
                          author_county_id=current_user.county.id,
                          day=current_user.county.kingdom.world.day)
        message.save()
        return redirect(url_for('overview', kingdom_id=kingdom_id, county_id=county_id))

    target_kingdom = Kingdom.query.filter_by(id=kingdom_id).first()
    target_county = County.query.filter_by(id=county_id).first()

    # Would like to move to a view_enemy route of some kind.
    # Ugly hack to return '{mobile/}gameplay/overview_enemy.html'
    template = '_enemy.'.join(template.split('.'))
    print(template)
    return render_template(template, target_kingdom=target_kingdom, target_county=target_county, form=form)
