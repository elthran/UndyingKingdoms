import functools

from flask import url_for
from flask_login import current_user
from werkzeug.utils import redirect


def in_active_session(func):
    """Implement in_active_session for any function."""

    @functools.wraps(func)
    def in_active_session_wrapper(*args, **kwargs):
        try:
            if not current_user.in_active_session:
                current_user.in_active_session = True
        except AttributeError:
            return redirect(url_for('login'))

        return func(*args, **kwargs)
    return in_active_session_wrapper
