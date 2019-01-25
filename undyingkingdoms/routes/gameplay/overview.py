from datetime import datetime

from flask import render_template, url_for, redirect
from flask_login import login_required, current_user

from undyingkingdoms import app
from undyingkingdoms.models import County, Kingdom, User, Message
from undyingkingdoms.models.forms.message import MessageForm


@app.route('/gameplay/overview/<int:kingdom_id>/<int:county_id>/', methods=['GET', 'POST'])
@login_required
def overview(kingdom_id=0, county_id=0):
    for user in User.query.filter_by(_in_active_session=True).all():
        time_since_last_activity = datetime.now() - user.time_modified
        if time_since_last_activity.total_seconds() > 300:  # A user who hasn't done anything in 5 minutes
            user.in_active_session = False
    if not current_user.in_active_session:
        current_user.in_active_session = True
    if not current_user.county:
        return redirect(url_for('initialize'))

    if kingdom_id == 0 or county_id == 0:
        has_mail = Message.query.filter_by(county_id=current_user.county.id, unread=True).count()
        return render_template('gameplay/overview.html', has_mail=has_mail)

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
    return render_template('gameplay/overview_enemy.html', target_kingdom=target_kingdom, target_county=target_county, form=form)
