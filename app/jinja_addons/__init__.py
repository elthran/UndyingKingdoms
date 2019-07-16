from flask import current_app
from markupsafe import Markup

from app import app
from app.serializers.vue_safe import vue_safe_array

___doc___ = """Add global filters and values to Jinja environment.

This must be imported after app config is loaded.
"""


@app.template_filter('vuesafe')
def vue_safe_filter(value):
    """Convert all tuples to lists.

    This also marks the value as safe to prevent escaping.
    I may need to make this more complex over time.
    """

    return Markup(vue_safe_array(value))


@app.context_processor
def inject_is_production():
    return dict(
        is_production=app.config['ENV'] == 'production'
    )
