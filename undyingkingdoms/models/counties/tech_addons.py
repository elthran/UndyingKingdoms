from random import choice

from sqlalchemy.ext.hybrid import hybrid_property

from tests import bp


def completed_techs_addon(cls):
    def get_completed_techs(self):
        """Return generator of completed technologies.

        Note: for reuse convert to list or set.
        """
        for tech in self.technologies.values():
            if tech.completed:
                yield tech

    cls.completed_techs = hybrid_property(get_completed_techs)


def incomplete_techs_addon(cls):
    def get_incomplete_techs(self):
        """Return generator of not completed technologies.

        Note: for reuse convert to list or set.
        """
        for tech in self.technologies.values():
            if not tech.completed:
                yield tech

    cls.incomplete_techs = hybrid_property(get_incomplete_techs)


def available_techs_addon(cls):
    def get_available_techs(self):
        """Generate incomplete techs with met requirements.

        Note: for reuse convert to list or set.
        """

        completed_techs = set(self.completed_techs)
        for tech in self.incomplete_techs:
            if not (set(tech.requirements) - completed_techs):
                yield tech

    cls.available_techs = hybrid_property(get_available_techs)


def unavailable_techs_addon(cls):
    def get_unavailable_techs(self):
        """Generate techs with unmet requirements.

        Note: returns a set.
        """

        return set(self.technologies.values()) - set(self.available_tech)

    cls.unavailable_techs = hybrid_property(get_unavailable_techs)


def advance_research(county):
    tech = county.research_choice
    tech.current += county.research
    if tech.current >= tech.cost:  # You save left over research
        county.research = tech.current - tech.cost
        tech.completed = True
        tech.activate(county)
        available_technologies = list(county.available_techs)
        if available_technologies:
            county.research_choice = choice(available_technologies)
        else:
            county.research = 0
    else:
        county.research = 0
