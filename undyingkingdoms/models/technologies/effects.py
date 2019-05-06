from ..interfaces import Command


class Effect(Command):
    county = object()

    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self.county, key, kwargs[key])

