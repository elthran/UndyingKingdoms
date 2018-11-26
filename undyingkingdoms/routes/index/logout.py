from flask import redirect, url_for
from flask_login import logout_user, current_user

from undyingkingdoms import app, db
from undyingkingdoms.models.sessions import Session


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    session = Session(current_user.id, "logout")
    db.session.add(session)
    db.session.commit()
    logout_user()
    return redirect(url_for('home'))
