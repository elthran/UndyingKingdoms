import datetime

from flask import render_template, url_for, redirect
from flask_login import login_required, current_user

from undyingkingdoms import app, db
from undyingkingdoms.models import County, Notification, DailyActiveUserEvent
from undyingkingdoms.models.forms.attack import TempGameAdvance


@login_required
@app.route('/gameplay/overview/', methods=['GET', 'POST'])
def overview():
    if not current_user.county:
        return redirect(url_for('initialize'))
    """
    Below is temporary hourly progression clock. Almost all the code here is temporary and scratch pad stuff.
    """
    time_keeper = County.query.filter_by(name="Time Warp").first()
    now = datetime.datetime.now().hour
    while now != time_keeper.total_land:
        for county in County.query.filter_by().all():
            county_dau = DailyActiveUserEvent(user_id=county.user_id)
            if county_dau.validate():
                db.session.add(county_dau)
                db.session.commit()
            notifications = county.change_day()
            for notification in notifications:
                db.session.add(notification)
        time_keeper.total_land = (time_keeper.total_land + 1) % 24
        time_keeper.kingdom.age += 1
        db.session.commit()
    form = TempGameAdvance()
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
    '''
    End of weird clock code
    '''
    return render_template('gameplay/overview.html', notifications=notifications, form=form)
