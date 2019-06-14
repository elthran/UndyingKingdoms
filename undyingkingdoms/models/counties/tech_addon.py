from random import choice

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm.collections import attribute_mapped_collection

from ..bases import db


def tech_addon(county_cls, tech_cls):
    """Establish a 1 to Many relationship between County and Technology."""
    county_cls.technologies = db.relationship(
        "Technology",
        collection_class=attribute_mapped_collection('key'),
        cascade="all, delete, delete-orphan",
        passive_deletes=True,
        order_by="Technology.tier",
        back_populates="county"
    )

    tech_cls.county_id = db.Column(db.Integer, db.ForeignKey('county.id', ondelete="CASCADE"), nullable=False)
    tech_cls.county = db.relationship(
        "County",
        back_populates="technologies"
    )

    def get_completed_techs(self):
        """Return generator of completed technologies.

        Note: for reuse convert to list or set.
        """
        for tech in self.technologies.values():
            if tech.completed:
                yield tech

    county_cls.completed_techs = hybrid_property(get_completed_techs)

    def get_incomplete_techs(self):
        """Return generator of not completed technologies.

        Note: for reuse convert to list or set.
        """
        for tech in self.technologies.values():
            if not tech.completed:
                yield tech

    county_cls.incomplete_techs = hybrid_property(get_incomplete_techs)

    def get_available_techs(self):
        """Generate incomplete techs with met requirements.

        Note: for reuse convert to list or set.
        """

        completed_techs = set(self.completed_techs)
        for tech in self.incomplete_techs:
            if not (set(tech.requirements) - completed_techs):
                yield tech

    county_cls.available_techs = hybrid_property(get_available_techs)

    def get_unavailable_techs(self):
        """Generate techs with unmet requirements.

        Note: returns a set.
        """

        return set(self.technologies.values()) - set(self.available_techs)

    county_cls.unavailable_techs = hybrid_property(get_unavailable_techs)

    def advance_research(self):
        tech = self.research_choice
        if tech is None:
            self.gold += self.research
            self.research = 0
            return None

        tech.current += self.research
        if tech.current >= tech.cost:  # You save left over research
            self.research = tech.current - tech.cost
            tech.current = tech.cost  # Remove the excess research as it looks off and is useless
            tech.completed = True
            tech.save()
            try:
                self.research_choice = choice(list(self.available_techs))
            except IndexError:
                self.research_choice = None

        self.research = 0

    county_cls.advance_research = advance_research
