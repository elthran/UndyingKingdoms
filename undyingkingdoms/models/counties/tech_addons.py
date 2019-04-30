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


def advance_research_addon(cls):
    def advance_research(self):
        technology = self.research_choice
        technology.current += self.research
        if technology.current >= technology.required:  # You save left over research
            self.research = technology.current - technology.required
            technology.completed = True
            available_technologies = list(self.available_techs)
            if available_technologies:
                self.research_choice = choice(available_technologies)
            else:
                self.research = 0
        else:
            self.research = 0

    cls.advance_research = advance_research

