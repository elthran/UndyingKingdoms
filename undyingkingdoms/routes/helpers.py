import functools
from datetime import datetime

from flask import url_for
from flask_login import current_user
from werkzeug.utils import redirect


def in_active_session(func):
    """Implement in_active_session for any function."""

    @functools.wraps(func)
    def in_active_session_wrapper(*args, **kwargs):
        try:
            current_user.time_modified = datetime.utcnow()
            if not current_user.in_active_session:
                current_user.in_active_session = True
        except AttributeError:
            return redirect(url_for('login'))

        return func(*args, **kwargs)
    return in_active_session_wrapper


def admin_required(func):
    """Implement in_active_session for any function."""

    @functools.wraps(func)
    def admin_required_wrapper(*args, **kwargs):
        try:
            if not current_user.is_admin:
                return redirect(url_for('overview', kingdom_id=0, county_id=0))
        except AttributeError:
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return admin_required_wrapper
