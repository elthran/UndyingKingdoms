from datetime import datetime

from flask import url_for, request, jsonify
from flask_login import current_user
from sqlalchemy.exc import DatabaseError
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from undyingkingdoms import app, db
from undyingkingdoms.routes.index.initialize import initialize


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

    if current_user.is_authenticated:
        current_user.time_modified = datetime.utcnow()
        if not current_user.in_active_session:
            try:
                current_user.in_active_session = True
            except Exception as ex:
                app.logger.critical("in_active_session setter is failing", str(ex))
            finally:
                return None
    return None


@app.before_request
def check_for_county():
    """Implement in_active_session for every request."""

    if current_user.is_authenticated:
        # print(request.endpoint)
        if current_user.county is None:
            return redirect(url_for('initialize'))
    return None
