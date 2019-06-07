from sqlalchemy.ext.hybrid import hybrid_property

from ..bases import GameEvent, db
import undyingkingdoms.models.effects as effect_module


class BaseTechnology(GameEvent):
    """An object that holds shared data between technologies.

    NOTE: when copied this object returns itself.
    """
    source = db.Column(db.String(32))
    output = db.Column(db.Float)  # output is depreciated
    cost = db.Column(db.Integer)
    max_level = db.Column(db.Integer)
    _description = db.Column(db.String(256))
    # TODO: make effects a string?
    _effects = db.Column(db.String(256))

    @hybrid_property
    def effects(self):
        """Extract Effect string and return it as an object."""
        code = compile(self._effects, '<string>', 'eval')
        return eval(code, effect_module.__dict__)

    @effects.setter
    def effects(self, value):
        """Save effects as a string.

        If effects isn't an iterable it will be coerced into one.
        """
        try:
            value = list(value)
        except TypeError:
            self._effects = repr([value])
            return
        self._effects = repr(value)

    @hybrid_property
    def description(self):
        """Map all effect kwargs into the description format string.

        Note that output is included as well.
        """

        all_kwargs = dict(output=self.output)
        # noinspection PyPropertyAccess
        for effect in self.effects:
            all_kwargs.update(effect.kwargs)
        code = compile('f' + repr(self._description), '<string>', 'eval')
        return eval(code, all_kwargs)

    @description.setter
    def description(self, value):
        """Save the description as a string..

        NOTE: I run compile on this to get some quick validation.
        The complied code isn't stored.
        """

        compile('f' + repr(value), '<string>', 'eval')

        self._description = value

    def __init__(self, source, cost, max_level, description,
                 effects):
        self.source = source
        self.cost = cost
        self.max_level = max_level
        self.description = description
        self.effects = effects

    def __copy__(self):
        return self

    # noinspection PyDefaultArgument
    def __deepcopy__(self, memodict={}):
        """This object returns self when copied.

        NOTE: if the session expires this will break when copied.
        """
        memodict[id(self)] = self
        return self

