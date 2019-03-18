def vue_safe_nbsp(s):
    """Returns a string with all spaces non-breaking.

    This string will render safely in vue.js
    """
    return '\u00a0'.join(s.split())


def vue_safe_metadata_mod(mod, county, is_percent=True):
    """Simplify a metatdata object to race and background.

    All values are assumed to be percents.
    """
    vue_safe_mod = {}
    race_mod = mod.get(county.race)
    background_mod = mod.get(county.background)
    if race_mod:
        value = int(race_mod[1] * 100) if is_percent else race_mod[1]
        vue_safe_mod['race'] = dict(
            name=vue_safe_nbsp(race_mod[0]),
            value=value
        )
    if background_mod:
        value = int(background_mod[1] * 100) if is_percent else background_mod[1]
        vue_safe_mod['background'] = dict(
            name=vue_safe_nbsp(background_mod[0]),
            value=value
        )

    return vue_safe_mod

def vue_safe_array(value):
    """Convert all tuples to lists.

    This also marks the value as safe to prevent escaping.
    I may need to make this more complex over time.
    """

    new = []
    if value is not None:
        for item in value:
            if isinstance(item, tuple):
                new.append(list(item))
            else:
                new.append(item)
        return new
    return None


def vue_safe_form(form):
    """A simplified form object suitable for vue.

    I might need to check type to accommodate other forms.
    """

    vs_form = {}

    for field in form:
        key = field.name
        if key != 'csrf_token':
            vs_form[key] = dict(
                choices = vue_safe_array(field.choices),
                id=key
            )
        else:
            vs_form[key] = dict(
                value=field.current_token,
                id=key,
                html=form.csrf_token
            )
    return vs_form
