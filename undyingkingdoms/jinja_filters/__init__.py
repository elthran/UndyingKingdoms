from markupsafe import Markup

from undyingkingdoms.blueprints.api.vue_safe import vue_safe_array

def vue_safe(value):
    """Convert all tuples to lists.

    This also marks the value as safe to prevent escaping.
    I may need to make this more complex over time.
    """

    return Markup(vue_safe_array(value))
