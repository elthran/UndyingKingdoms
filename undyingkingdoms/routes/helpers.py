import functools

from flask import url_for
from flask_login import current_user
from werkzeug.utils import redirect


def admin_required(func):
    """Implement admin required for any function."""

    @functools.wraps(func)
    def admin_required_wrapper(*args, **kwargs):
        try:
            if not current_user.is_admin:
                return redirect(url_for('overview', kingdom_id=0, county_id=0))
        except AttributeError:
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return admin_required_wrapper
