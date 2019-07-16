import warnings

from sqlalchemy.ext.hybrid import hybrid_property

from app.models.notifications import Notification
from ..bases import GameEvent, db
import app.models.effects as effect_module

technology_to_technology = db.Table(
    "technology_to_technology", db.metadata,
    # don't really understand enough to name these properly
    db.Column("left_node_id", db.Integer, db.ForeignKey("technology.id"), primary_key=True),
    db.Column("right_node_id", db.Integer, db.ForeignKey("technology.id"), primary_key=True)
)


class Technology(GameEvent):
    name = db.Column(db.String(64))
    tier = db.Column(db.Integer)
    world_day = db.Column(db.Integer)  # Day you started to research
    county_day = db.Column(db.Integer)
    current = db.Column(db.Integer)
    _completed = db.Column(db.Boolean)

    # generic, could be shared
    source = db.Column(db.String(32))
    output = db.Column(db.Float)  # output is depreciated
    cost = db.Column(db.Integer)
    max_level = db.Column(db.Integer)
    _description = db.Column(db.String(256))
    _effects = db.Column(db.String(256))

    requirements = db.relationship(
        "Technology",
        secondary="technology_to_technology",
        primaryjoin="Technology.id==technology_to_technology.c.left_node_id",
        secondaryjoin="Technology.id==technology_to_technology.c.right_node_id",
        backref="requirees"
    )

    @hybrid_property
    def completed(self):
        return self._completed

    @completed.setter
    def completed(self, value):
        """Toggle tech activation when you complete it."""
        if value is True:
            self.activate(self.county)
        else:
            self.deactivate(self.county)
        self._completed = value

    @hybrid_property
    def key(self):
        return self.name.lower()

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

    # noinspection PyUnresolvedReferences,PyMethodParameters
    @effects.expression
    def effects(cls):
        return cls._effects

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

    # noinspection PyUnresolvedReferences,PyMethodParameters
    @description.expression
    def description(cls):
        return cls._description

    def __init__(self, name, cost, max_level, description, requirements=None,
                 tier=1, effects=None, source="Generic"):
        if requirements is None:
            requirements = []
        if effects is None:
            effects = []

        self.name = name
        self.tier = tier
        self.world_day = None
        self.county_day = None
        self.current = 0
        self._completed = False
        self.requirements = requirements

        # could be shared
        self.source = source
        self.cost = cost
        self.max_level = max_level
        self.description = description
        self.effects = effects

    @staticmethod
    def establish_requirements(technologies, metadata):
        """Merge a dict of requirements with a dict of technologies.

        When a requirement doesn't exist a new tech should be added
        to the user.
        """
        for key in metadata:
            assert type(metadata[key]) != str
            for requirement in metadata[key]:
                try:
                    technologies[key].requirements.append(technologies[requirement])
                except KeyError:
                    message = f'Tech "{key}" -> "{requirement} relationship is failing.'
                    warnings.warn(message, RuntimeWarning)
                    pass  # add new tech to technologies

    def activate(self, county):
        # noinspection PyPropertyAccess
        for effect in self.effects:
            try:
                effect.activate(county)
            except TypeError as ex:
                tech_name = self.name
                effect_info = repr(effect.kwargs)
                # noinspection PyPropertyAccess
                description = self.description
                county_name = county.name
                raise TypeError(
                    f"Tech: {tech_name} of {description} was crashed "
                    f"by {effect_info} in county {county_name}"
                    f"\nThe original exception was\n{ex}"
                )

        # noinspection PyPropertyAccess
        notice = Notification(
            county,
            f"Discovered {self.name}",
            self.description,
            category="Research"
        )
        notice.save()

    def deactivate(self, county):
        # noinspection PyPropertyAccess
        for effect in self.effects:
            effect.undo(county)

        # noinspection PyPropertyAccess
        notice = Notification(
            county,
            f"Lost {self.name}",
            self.description,
            category="Research"
        )
        notice.save()
