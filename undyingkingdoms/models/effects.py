import operator

from .interfaces import EffectInterface
import undyingkingdoms.models as udk_models
models = lambda: udk_models.exports


def relative_lookup(cls_name):
    """Look up a model from the model exports file.

    e.g.
        'Wizardry' => exports.Wizardry
    """

    return getattr(models(), cls_name)


class Effect:
    def __init__(self, cls_name="County", **kwargs):
        self.cls_name = cls_name
        self.kwargs = kwargs

    def general_activate(self, op=operator.add):
        obj = relative_lookup(self.cls_name)
        for key in self.kwargs:
            try:
                initial_val = getattr(obj, '_' + key)
            except AttributeError:
                initial_val = getattr(obj, key)
            setattr(
                obj,
                key,
                op(initial_val, self.kwargs[key])
            )

    def __repr__(self):
        class_name = self.__class__.__name__
        attr = self.cls_name
        kwargs = ', '.join(f'{k}={v}' for k, v in self.kwargs.items())
        return f"{class_name}({attr!r}, {kwargs})"


class Add(Effect, EffectInterface):
    """Increase an obj value by a given amount.

    Does  obj.x += y
    """

    def activate(self, obj):
        self.general_activate(op=operator.add)

    def undo(self, obj):
        minus = Minus(self.cls_name, **self.kwargs)
        minus.activate(obj)


class Minus(Effect, EffectInterface):
    """Decrease an obj value by a given amount.

    Does  obj.x -= y
    """

    def activate(self, obj):
        self.general_activate(op=operator.sub)

    def undo(self, obj):
        add = Add(self.cls_name, **self.kwargs)
        add.activate(obj)


class Times(Effect, EffectInterface):
    """Increase an obj value by a given percent.

    Does  obj.x *= 1 + y
    """

    def activate(self, obj):
        self.general_activate(op=lambda a, b: a * (1 + b))

    def undo(self, obj):
        divide = Divide(self.cls_name, **self.kwargs)
        divide.activate(obj)


class Divide(Effect, EffectInterface):
    """Decrease an obj value by a given percent.

    Does  obj.x /= 1 + y
    """

    def activate(self, obj):
        self.general_activate(op=lambda a, b: a / (1 + b))

    def undo(self, obj):
        times = Times(self.cls_name, **self.kwargs)
        times.activate(obj)
