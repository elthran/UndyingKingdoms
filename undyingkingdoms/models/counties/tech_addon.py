from random import choice

from ..bases import db


def tech_addon(cls):
    def get_completed_techs(self):
        """Return generator of completed technologies.

        Note: for reuse convert to list or set.
        """
        for tech in self.technologies.values():
            if tech.completed:
                yield tech

    cls.completed_techs = db.hybrid_property(get_completed_techs)

    def get_incomplete_techs(self):
        """Return generator of not completed technologies.

        Note: for reuse convert to list or set.
        """
        for tech in self.technologies.values():
            if not tech.completed:
                yield tech

    cls.incomplete_techs = db.hybrid_property(get_incomplete_techs)

    def get_available_techs(self):
        """Generate incomplete techs with met requirements.

        Note: for reuse convert to list or set.
        """

        completed_techs = set(self.completed_techs)
        for tech in self.incomplete_techs:
            if not (set(tech.requirements) - completed_techs):
                yield tech

    cls.available_techs = db.hybrid_property(get_available_techs)

    def get_unavailable_techs(self):
        """Generate techs with unmet requirements.

        Note: returns a set.
        """

        return set(self.technologies.values()) - set(self.available_tech)

    cls.unavailable_techs = db.hybrid_property(get_unavailable_techs)

    def advance_research(self):
        tech = self.research_choice
        tech.current += self.research
        if tech.current >= tech.cost:  # You save left over research
            self.research = tech.current - tech.cost
            tech.completed = True
            tech.activate(self)
            available_technologies = list(self.available_techs)
            if available_technologies:
                self.research_choice = choice(available_technologies)
            else:
                self.research = 0
        else:
            self.research = 0

    cls.advance_research = advance_research
