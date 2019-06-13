from random import choice

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm.collections import attribute_mapped_collection

from ..bases import db


def technology_addon(county_cls, tech_cls):
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

    def get_completed_technologies(self):
        """Return generator of completed technologies.

        Note: for reuse convert to list or set.
        """
        for tech in self.technologies.values():
            if tech.completed:
                yield tech

    county_cls.completed_technologies = hybrid_property(get_completed_technologies)

    def get_incomplete_technologies(self):
        """Return generator of not completed technologies.

        Note: for reuse convert to list or set.
        """
        for tech in self.technologies.values():
            if not tech.completed:
                yield tech

    county_cls.incomplete_technologies = hybrid_property(get_incomplete_technologies)

    def get_available_technologies(self):
        """Generate incomplete technologies with met requirements.

        Note: for reuse convert to list or set.
        """

        completed_technologies = set(self.completed_technologies)
        for tech in self.incomplete_technologies:
            if not (set(tech.requirements) - completed_technologies):
                yield tech

    county_cls.available_technologies = hybrid_property(get_available_technologies)

    def get_unavailable_technologies(self):
        """Generate technologies with unmet requirements.

        Note: returns a set.
        """

        return set(self.technologies.values()) - set(self.available_technologies)

    county_cls.unavailable_technologies = hybrid_property(get_unavailable_technologies)

    def advance_research(self):
        tech = self.research_choice
        if tech is None:
            # Should add a Notification here saying you get gold instead of research
            self.gold += self.research
        else:
            tech.current += self.research
            if tech.current >= tech.cost:  # You save left over research
                self.research = tech.current - tech.cost
                tech.current = tech.cost  # Remove the excess research as it looks off and is useless
                tech.completed = True
                try:
                    available_technologies = list(self.available_technologies)
                    self.research_choice = choice(available_technologies)
                except AttributeError:
                    available_technologies = []
                    self.gold += self.research
                    self.research = 0
                    self.research_choice = None
            else:
                self.research = 0

    county_cls.advance_research = advance_research
