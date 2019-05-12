from .interfaces import EffectInterface


class Plequals(EffectInterface):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def activate(self, obj):
        for key in self.kwargs:
            setattr(
                obj,
                key,
                getattr(obj, key) + self.kwargs[key]
            )

    def undo(self, obj):
        neffect = Nequals(**self.kwargs)
        neffect.activate(obj)


class Nequals(EffectInterface):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def activate(self, obj):
        for key in self.kwargs:
            setattr(
                obj,
                key,
                getattr(obj, key) - self.kwargs[key]
            )

    def undo(self, obj):
        peffect = Plequals(**self.kwargs)
        peffect.activate(obj)


class Mequals(EffectInterface):
    def __init__(self, **kwargs):
        """Increase a obj value by a give percent.


        Does  x *= 1 + y
        :param obj:
        :param kwargs: any obj attribute to multiply by
        """
        self.kwargs = kwargs

    def activate(self, obj):
        for key in self.kwargs:
            setattr(
                obj,
                key,
                getattr(obj, key) * (1 + self.kwargs[key])
            )

    def undo(self, obj):
        deffect = Dequals(**self.kwargs)
        deffect.activate(obj)


class Dequals(EffectInterface):
    def __init__(self, **kwargs):
        """Decrease a obj value by a give percent.


        Does  x /= 1 + y
        :param obj:
        :param kwargs: any obj attribute to multiply by
        """
        self.kwargs = kwargs

    def activate(self, obj):
        for key in self.kwargs:
            setattr(
                obj,
                key,
                getattr(obj, key) / (1 + self.kwargs[key])
            )

    def undo(self, obj):
        meffect = Mequals(**self.kwargs)
        meffect.activate(obj)
