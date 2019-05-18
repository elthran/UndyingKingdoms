from tests import bp
from .interfaces import EffectInterface

def relative_lookup(obj, attr):
    """Look up a sub-table on this object.

    e.g.
        county.wizardry

    Later I hope to be able to handle multiple "." in the name.
    """
    if attr != ".":
        return getattr(obj, attr)
    return obj


class EffectInit:
    def __init__(self, attr=".", **kwargs):
        self.attr = attr
        self.kwargs = kwargs


class Add(EffectInit, EffectInterface):
    """Increase an obj value by a given amount.

    Does  obj.x += y
    """
    def activate(self, obj):
        obj = relative_lookup(obj, self.attr)
        for key in self.kwargs:
            try:
                initial_val = getattr(obj, '_' + key)
            except AttributeError:
                initial_val = getattr(obj, key)
            setattr(
                obj,
                key,
                initial_val + self.kwargs[key]
            )

    def undo(self, obj):
        minus = Minus(self.attr, **self.kwargs)
        minus.activate(obj)


class Minus(EffectInit, EffectInterface):
    """Decrease an obj value by a given amount.

    Does  obj.x -= y
    """
    def activate(self, obj):
        obj = relative_lookup(obj, self.attr)
        for key in self.kwargs:
            setattr(
                obj,
                key,
                getattr(obj, key) - self.kwargs[key]
            )

    def undo(self, obj):
        add = Add(self.attr, **self.kwargs)
        add.activate(obj)


class Times(EffectInit, EffectInterface):
    """Increase an obj value by a given percent.

    Does  obj.x *= 1 + y
    """
    def activate(self, obj):
        obj = relative_lookup(obj, self.attr)
        for key in self.kwargs:
            setattr(
                obj,
                key,
                getattr(obj, key) * (1 + self.kwargs[key])
            )

    def undo(self, obj):
        divide = Divide(self.attr, **self.kwargs)
        divide.activate(obj)


class Divide(EffectInit, EffectInterface):
    """Decrease an obj value by a given percent.

    Does  obj.x /= 1 + y
    """

    def activate(self, obj):
        obj = relative_lookup(obj, self.attr)
        for key in self.kwargs:
            setattr(
                obj,
                key,
                getattr(obj, key) / (1 + self.kwargs[key])
            )

    def undo(self, obj):
        times = Times(self.attr, **self.kwargs)
        times.activate(obj)
