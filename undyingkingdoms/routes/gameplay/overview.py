from flask import render_template, request, url_for, redirect
from flask_login import login_required, current_user

from undyingkingdoms import app, db
from undyingkingdoms.models import County, Notification, DailyActiveUserEvent
from undyingkingdoms.models.forms.login import Testing


@login_required
@app.route('/gameplay/overview/', methods=['GET', 'POST'])
def overview():
    form = Testing(request.form)
    if form.validate_on_submit():
        for county in County.query.filter_by().all():
            county_dau = DailyActiveUserEvent(user_id=county.user_id)
            if county_dau.validate():
                db.session.add(county_dau)
                db.session.commit()
            notifications = county.change_day()
            for notification in notifications:
                db.session.add(notification)
            db.session.commit()
    notifications = current_user.county.notifications
    for notification in Notification.query.filter_by(county_id=current_user.county.id).all():
        db.session.delete(notification)
        db.session.commit()
    if not current_user.county:
        return redirect(url_for('initialize'))
    return render_template('gameplay/overview.html', form=form, notifications=notifications)
