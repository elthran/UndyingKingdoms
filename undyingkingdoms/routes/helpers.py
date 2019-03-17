import functools
import types

from flask import url_for, request
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


def mobile_on_vue(endpoint, **options):
    """Implement redirect to mobile vue site for any function.

    Passing any null value for endpoint defaults it the that function url.
    e.g.
    @mobile_on_vue
    def infrastructure():
        pass

    will send url_for('infrastructure') to the mobile vue site.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if request.MOBILE:
                # slice of leading / to prevent //
                path = url_for(endpoint or func.__name__, **options)[1:]
                return redirect(url_for('mobile', path=path))
            return func(*args, **kwargs)
        return wrapper

    if isinstance(endpoint, types.FunctionType):
        func, endpoint = endpoint, None
        return decorator(func)
    return decorator
