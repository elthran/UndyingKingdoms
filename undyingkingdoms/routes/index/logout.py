from flask import redirect, url_for
from flask_login import logout_user, current_user

from undyingkingdoms.models import County
from undyingkingdoms.models.analytics import AuthenticationEvent
from undyingkingdoms import app, db
from undyingkingdoms.models.bases import GameEvent
from undyingkingdoms.models.dau import DailyActiveUserEvent


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    authentication_event = AuthenticationEvent(user_id=current_user.id,
                                               activity="logout",
                                               session_id=current_user.session_id)
    db.session.add(authentication_event)
    db.session.commit()
    logout_user()
    counties = County.query.all()
    for county in counties:
        event = DailyActiveUserEvent(user_id=county.user_id)
        event.get_daily_stats()
        if event.validate():
            db.session.add(event)
            db.session.commit()
    return redirect(url_for('home'))
