import warnings

from sqlalchemy.ext.hybrid import hybrid_property

from undyingkingdoms.models.notifications import Notification
from ..bases import GameEvent, db
from .base_technology import BaseTechnology

tech_to_tech = db.Table(
    "tech_to_tech", db.metadata,
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

    requirements = db.relationship(
        "Technology",
        secondary="tech_to_tech",
        primaryjoin="Technology.id==tech_to_tech.c.left_node_id",
        secondaryjoin="Technology.id==tech_to_tech.c.right_node_id",
        backref="requirees"
    )

    base_id = db.Column(db.Integer, db.ForeignKey('base_technology.id'))
    base = db.relationship("BaseTechnology")

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
    def source(self):
        return self.base.source

    @hybrid_property
    def cost(self):
        return self.base.cost

    @hybrid_property
    def max_level(self):
        return self.base.max_level

    @hybrid_property
    def effects(self):
        # noinspection PyPropertyAccess
        return self.base.effects

    @hybrid_property
    def description(self):
        # noinspection PyPropertyAccess
        return self.base.description

    @db.reconstructor
    def init_on_load(self):
        # noinspection PyAttributeOutsideInit
        self.notifier = Notification

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

        self.base = BaseTechnology(
            source,
            cost,
            max_level,
            description,
            effects,
        )
        self.init_on_load()

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
            try:
                effect.activate(county)
            except TypeError as ex:
                tech_name = self.name
                effect_info = repr(effect.kwargs)
                description = self.description
                county_name = county.name
                raise TypeError(
                    f"Tech: {tech_name} of {description} was crashed "
                    f"by {effect_info} in county {county_name}"
                    f"\nThe original exception was\n{ex}"
                )

        notice = self.notifier(
            county,
            f"Discovered {self.name}",
            self.description,
            category="Research"
        )
        notice.save()

    def deactivate(self, county):
        for effect in self.effects:
            effect.undo(county)

        notice = self.notifier(
            county,
            f"Lost {self.name}",
            self.description,
            category="Research"
        )
        notice.save()
