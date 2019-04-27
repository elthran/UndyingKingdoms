import functools


def preferences_init_addon(county_cls, preferences_cls):
    def preferences_init(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0]  # I think?
            result = func(*args, **kwargs)
            preferences_cls(self, self.user)  # hopefully this works.
            return result
        return wrapper

    county_cls.__init__ = preferences_init(county_cls.__init__)
