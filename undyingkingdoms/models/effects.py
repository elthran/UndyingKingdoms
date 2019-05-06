from .interfaces import EffectInterface


class PlequalsEffect(EffectInterface):
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
        neffect = NequalsEffect(**self.kwargs)
        neffect.activate(obj)


class NequalsEffect(EffectInterface):
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
        peffect = PlequalsEffect(**self.kwargs)
        peffect.activate(obj)


class MequalsEffect(EffectInterface):
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
        deffect = DequalsEffect(**self.kwargs)
        deffect.activate(obj)


class DequalsEffect(EffectInterface):
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
        meffect = MequalsEffect(**self.kwargs)
        meffect.activate(obj)
