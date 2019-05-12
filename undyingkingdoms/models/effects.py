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


class Plequals(EffectInit, EffectInterface):
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
        neffect = Nequals(self.attr, **self.kwargs)
        neffect.activate(obj)


class Nequals(EffectInit, EffectInterface):
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
        peffect = Plequals(self.attr, **self.kwargs)
        peffect.activate(obj)


class Mequals(EffectInit, EffectInterface):
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
        deffect = Dequals(self.attr, **self.kwargs)
        deffect.activate(obj)


class Dequals(EffectInit, EffectInterface):
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
        meffect = Mequals(self.attr, **self.kwargs)
        meffect.activate(obj)
