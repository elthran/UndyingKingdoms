from sqlalchemy.ext.hybrid import hybrid_property

from undyingkingdoms.models.bases import GameEvent, db


class BaseTechnology(GameEvent):
    source = db.Column(db.String(32))
    output = db.Column(db.Float)  # output is depreciated
    cost = db.Column(db.Integer)
    max_level = db.Column(db.Integer)
    _description = db.Column(db.String(256))
    # TODO: make effects a string?
    effects = db.Column(db.PickleType)

    @db.validates('effects')
    def validate_effects(self, key, effects):
        try:
            _ = (e for e in effects)
        except TypeError:
            return [effects]
        return effects

    @hybrid_property
    def description(self):
        """Map all effect kwargs into the description format string.

        Note that output is included as well.
        """

        all_kwargs = dict(output=self.output)
        for effect in self.effects:
            all_kwargs.update(effect.kwargs)
        code = compile(self._description, '<string>', 'eval')
        return eval(code, all_kwargs)

    @description.setter
    def description(self, value):
        """Compile description into a format string.

        This has the added bonus of validating all format code.
        """
        # validate format code, but otherwise do nothing.
        # I haven't worked out how to store code objects yet.
        compile('f' + repr(value), '<string>', 'eval')
        self._description = 'f' + repr(value)

    def __init__(self, source, cost, max_level, description,
                 effects):
        self.source = source
        self.cost = cost
        self.max_level = max_level
        self.description = description
        self.effects = effects
