from flask import render_template, request
from flask_login import login_required, current_user
from undyingkingdoms import app, db
from undyingkingdoms.models import County, Notification
from undyingkingdoms.models.forms.login import Testing


@login_required
@app.route('/gameplay/overview', methods=['GET', 'POST'])
def overview():
    form = Testing(request.form)
    if form.validate_on_submit():
        for county in County.query.filter_by().all():
            notifications = county.change_day()
            for notification in notifications:
                db.session.add(notification)
            db.session.commit()
    notifications = current_user.county.notifications
    for notification in Notification.query.filter_by(county_id=current_user.county.id).all():
        db.session.delete(notification)
        db.session.commit()
    return render_template('gameplay/overview.html', form=form, notifications=notifications)
