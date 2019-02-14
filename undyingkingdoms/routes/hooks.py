from datetime import datetime

from flask import url_for
from flask_login import current_user
from sqlalchemy.exc import DatabaseError
from werkzeug.utils import redirect

from undyingkingdoms import app, db


@app.after_request
def session_commit(response):
    if response.status_code >= 400:
        # I'm not sure if this is correct?
        # Maybe should redirect to 404?
        return response
    try:
        db.session.commit()
    except DatabaseError:
        db.session.rollback()
        raise
    # db.session.remove() # is called for you by flask-sqlalchemy
    return response


@app.before_request
def in_active_session():
    """Implement in_active_session for every request."""

    try:
        current_user.time_modified = datetime.utcnow()
        if not current_user.in_active_session:
            current_user.in_active_session = True
    except AttributeError:
        pass
    return None
