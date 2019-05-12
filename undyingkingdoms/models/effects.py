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
            setattr(
                obj,
                key,
                getattr(obj, key) + self.kwargs[key]
            )

    def undo(self, obj):
        neffect = Minus(self.attr, **self.kwargs)
        neffect.activate(obj)


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
        peffect = Add(self.attr, **self.kwargs)
        peffect.activate(obj)


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
        deffect = Divide(self.attr, **self.kwargs)
        deffect.activate(obj)


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
        meffect = Times(self.attr, **self.kwargs)
        meffect.activate(obj)
