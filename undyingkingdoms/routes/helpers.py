import functools

from flask import url_for
from flask_login import current_user
from werkzeug.utils import redirect

from undyingkingdoms.models import County


def admin_required(func):
    """Implement admin required for any function."""

    @functools.wraps(func)
    def admin_required_wrapper(*args, **kwargs):
        try:
            if not current_user.is_admin:
                return redirect(url_for('overview'))
        except AttributeError:
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return admin_required_wrapper

def not_allies(func):
    """Implement diplomatic security of allied kingdoms.

    Requires: county_id parameter in kwargs.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            target = County.query.get(kwargs['county_id'])
        except KeyError:
            raise KeyError('You need to add a "county_id" field to this route.')
        kingdom = current_user.county.kingdom
        if target.kingdom in kingdom.allies:
            return redirect(url_for('overview'))
        return func(*args, **kwargs)
    return wrapper


def not_self(func):
    """Implement diplomatic security of allied kingdoms.

    Requires: county_id parameter in kwargs.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            if kwargs['county_id'] == current_user.county.id:
                return redirect(url_for('overview'))
        except KeyError:
            raise KeyError('You need to add a "county_id" field to this route.')

        return func(*args, **kwargs)
    return wrapper
