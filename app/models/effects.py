import operator

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from lib.namers import to_var_name
from .interfaces import EffectInterface
import app.models as udk_models
models = lambda: udk_models.exports


def relative_lookup(instance, cls_name):
    """Look up a model from the model exports file.

    e.g.
        'Wizardry' => exports.Wizardry
    """
    cls = getattr(models(), cls_name)

    # simple join
    instance_cls_name_as_var = to_var_name(instance.__class__.__name__)
    instance_as_foreign_key = f'{instance_cls_name_as_var}_id'
    possible_join = {instance_as_foreign_key: instance.id}
    try:
        return cls.query.filter_by(**possible_join).one()
    except NoResultFound:
        pass
    except InvalidRequestError:
        pass

    # complex join
    instance_foreign_keys = {key for key in instance.__dict__.keys() if key.endswith('_id')}
    cls_foreign_keys = {key for key in cls.__dict__.keys() if key.endswith('_id')}
    intersecting_foreign_keys = instance_foreign_keys & cls_foreign_keys
    for key in intersecting_foreign_keys:
        possible_join = {key: getattr(instance, key)}
        try:
            return cls.query.filter_by(**possible_join).one()
        except NoResultFound:
            pass
        except InvalidRequestError:
            pass
    raise ValueError(
        f"No connection was found between {instance} and {cls}."
        " You need to debug Effect activation between these objects."
    )


class Effect:
    def __init__(self, cls_name="County", **kwargs):
        self.cls_name = cls_name
        self.kwargs = kwargs

    def general_activate(self, instance, op=operator.add):
        obj = relative_lookup(instance, self.cls_name)
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

    def activate(self, instance):
        self.general_activate(instance, op=operator.add)

    def undo(self, county):
        minus = Minus(self.cls_name, **self.kwargs)
        minus.activate(county)


class Minus(Effect, EffectInterface):
    """Decrease an obj value by a given amount.

    Does  obj.x -= y
    """

    def activate(self, county):
        self.general_activate(county, op=operator.sub)

    def undo(self, county):
        add = Add(self.cls_name, **self.kwargs)
        add.activate(county)


class Times(Effect, EffectInterface):
    """Increase an obj value by a given percent.

    Does  obj.x *= 1 + y
    """

    def activate(self, county):
        self.general_activate(county, op=lambda a, b: a * (1 + b))

    def undo(self, county):
        divide = Divide(self.cls_name, **self.kwargs)
        divide.activate(county)


class Divide(Effect, EffectInterface):
    """Decrease an obj value by a given percent.

    Does  obj.x /= 1 + y
    """

    def activate(self, county):
        self.general_activate(county, op=lambda a, b: a / (1 + b))

    def undo(self, county):
        times = Times(self.cls_name, **self.kwargs)
        times.activate(county)
