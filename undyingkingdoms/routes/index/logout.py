from flask import redirect, url_for
from flask_login import logout_user, current_user
from undyingkingdoms.models.analytics import AuthenticationEvent
from undyingkingdoms import app, db
from undyingkingdoms.models.bases import GameEvent


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    authentication_event = AuthenticationEvent(user_id=current_user.id, activity="logout")
    if not authentication_event.validity:
        authentication_event = GameEvent(activity="invalid_login")
    db.session.add(authentication_event)
    db.session.commit()
    logout_user()
    return redirect(url_for('home'))
