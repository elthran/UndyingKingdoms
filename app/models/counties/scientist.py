from sqlalchemy.ext.hybrid import hybrid_property

from ..bases import GameEvent, db


class Scientist(GameEvent):
    _research_change = db.Column(db.Integer)
    research_multiplier = db.Column(db.Integer)

    @hybrid_property
    def research_change(self):
        county = self.county
        building_production = county.buildings['lab'].total * (county.buildings['lab'].output + self.research_multiplier)
        return building_production + self._research_change

    @research_change.setter
    def research_change(self, value):
        self._research_change = value

    # noinspection PyUnresolvedReferences
    @research_change.expression
    def research_change(self):
        return self._research_change

    def __init__(self, county):
        self.county = county
        self.research_change = 0
        self.research_multiplier = 0
