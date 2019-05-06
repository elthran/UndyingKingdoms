from sqlalchemy.ext.hybrid import hybrid_property

from ..bases import GameEvent, db


class Technology(GameEvent):
    county_id = db.Column(db.Integer, db.ForeignKey('county.id', ondelete="CASCADE"), nullable=False)
    world_day = db.Column(db.Integer)  # Day you started to research
    county_day = db.Column(db.Integer)
    name = db.Column(db.String(64))
    current = db.Column(db.Integer)
    tier = db.Column(db.Integer)
    output = db.Column(db.Float)
    cost = db.Column(db.Integer)
    level = db.Column(db.Integer)
    max_level = db.Column(db.Integer)
    completed = db.Column(db.Boolean)
    _description = db.Column(db.String(128))
    effects = db.Column(db.PickleType)

    requirement_id = db.Column(db.Integer, db.ForeignKey('technology.id'))
    requirements = db.relationship("Technology")

    @db.validates('effects')
    def validate_effects(self, key, effects):
        if effects.__class__ != list:
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
        return self._description.format(**all_kwargs)

    def __init__(self, name, cost, max_level, description, requirements=None, tier=1, output=None, effects=None):
        if requirements is None:
            requirements = []
        if effects is None:
            effects = []

        self.world_day = None
        self.county_day = None
        self.name = name
        self.current = 0
        self.cost = cost
        self.level = 0
        self.tier = tier
        self.output = output
        self.max_level = max_level
        self.completed = False
        self._description = description
        self.requirements = requirements
        self.effects = effects

    @staticmethod
    def establish_requirements(techs, metadata):
        """Merge a dict of requirements with a dict of technologies.

        When a requirement doesn't exist a new tech should be added
        to the user.
        """
        for key in metadata:
            for requirement in metadata[key]:
                try:
                    techs[key].requirements.append(techs[requirement])
                except KeyError:
                    pass  # add new tech to techs

    def activate(self, county):
        for effect in self.effects:
            effect.execute(county)
