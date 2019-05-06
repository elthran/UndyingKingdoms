from ..interfaces import EffectInterface


class PlequalsEffect(EffectInterface):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def activate(self, county):
        for key in self.kwargs:
            setattr(
                county,
                key,
                getattr(county, key) + self.kwargs[key]
            )

    def undo(self, county):
        neffect = NequalsEffect(**self.kwargs)
        neffect.activate(county)


class NequalsEffect(EffectInterface):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def activate(self, county):
        for key in self.kwargs:
            setattr(
                county,
                key,
                getattr(county, key) - self.kwargs[key]
            )

    def undo(self, county):
        peffect = PlequalsEffect(**self.kwargs)
        peffect.activate(county)


class MequalsEffect(EffectInterface):
    def __init__(self, **kwargs):
        """Increase a county value by a give percent.


        Does  x *= 1 + y
        :param county:
        :param kwargs: any county attribute to multiply by
        """
        self.kwargs = kwargs

    def activate(self, county):
        for key in self.kwargs:
            setattr(
                county,
                key,
                getattr(county, key) * (1 + self.kwargs[key])
            )

    def undo(self, county):
        deffect = DequalsEffect(**self.kwargs)
        deffect.activate(county)


class DequalsEffect(EffectInterface):
    def __init__(self, **kwargs):
        """Decrease a county value by a give percent.


        Does  x /= 1 + y
        :param county:
        :param kwargs: any county attribute to multiply by
        """
        self.kwargs = kwargs

    def activate(self, county):
        for key in self.kwargs:
            setattr(
                county,
                key,
                getattr(county, key) / (1 + self.kwargs[key])
            )

    def undo(self, county):
        meffect = MequalsEffect(**self.kwargs)
        meffect.activate(county)
