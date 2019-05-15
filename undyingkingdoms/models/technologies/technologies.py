import warnings

from sqlalchemy.ext.hybrid import hybrid_property

from tests import bp
from undyingkingdoms.models.notifications import Notification
from ..bases import GameEvent, db

tech_to_tech = db.Table(
    "tech_to_tech", db.metadata,
    # don't really understand enough to name these properly
    db.Column("left_node_id", db.Integer, db.ForeignKey("technology.id"), primary_key=True),
    db.Column("right_node_id", db.Integer, db.ForeignKey("technology.id"), primary_key=True)
)


class Technology(GameEvent):
    world_day = db.Column(db.Integer)  # Day you started to research
    county_day = db.Column(db.Integer)
    name = db.Column(db.String(64))
    source = db.Column(db.String(32))
    current = db.Column(db.Integer)
    tier = db.Column(db.Integer)
    output = db.Column(db.Float)
    cost = db.Column(db.Integer)
    level = db.Column(db.Integer)
    max_level = db.Column(db.Integer)
    _completed = db.Column(db.Boolean)
    _description = db.Column(db.String(128))
    effects = db.Column(db.PickleType)

    requirements = db.relationship(
        "Technology",
        secondary="tech_to_tech",
        primaryjoin="Technology.id==tech_to_tech.c.left_node_id",
        secondaryjoin="Technology.id==tech_to_tech.c.right_node_id",
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

    @db.validates('effects')
    def validate_effects(self, key, effects):
        try:
            _ = (e for e in effects)
        except TypeError:
            return [effects]
        return effects

    @hybrid_property
    def key(self):
        return self.name.lower()

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

    def __init__(self, name, cost, max_level, description, requirements=None,
                 tier=1, output=None, effects=None, source="Generic"):
        if requirements is None:
            requirements = []
        if effects is None:
            effects = []

        self.world_day = None
        self.county_day = None
        self.name = name
        self.source = source
        self.current = 0
        self.cost = cost
        self.level = 0
        self.tier = tier
        self.output = output
        self.max_level = max_level
        self._completed = False
        self.description = description
        self.requirements = requirements
        self.effects = effects

    @staticmethod
    def establish_requirements(techs, metadata):
        """Merge a dict of requirements with a dict of technologies.

        When a requirement doesn't exist a new tech should be added
        to the user.
        """
        for key in metadata:
            assert type(metadata[key]) != str
            for requirement in metadata[key]:
                try:
                    techs[key].requirements.append(techs[requirement])
                except KeyError:
                    message = f'Tech "{key}" -> "{requirement} relationship is failing.'
                    warnings.warn(message, RuntimeWarning)
                    pass  # add new tech to techs

    def activate(self, county):
        for effect in self.effects:
            effect.activate(county)

        notice = Notification(
            county,
            f"Discovered {self.name}",
            self.description,
            category="Research"
        )
        notice.save()

    def deactivate(self, county):
        for effect in self.effects:
            effect.undo(county)

        notice = Notification(
            county,
            f"Lost {self.name}",
            self.description,
            category="Research"
        )
        notice.save()
