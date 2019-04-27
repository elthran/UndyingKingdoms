import functools

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
        bp()
        completed_techs = set(self.completed_techs)
        for tech in self.incomplete_techs:
            if not (set(tech.requirements) - completed_techs):
                yield tech

    cls.available_techs = hybrid_property(get_available_techs)


def advance_research_addon(cls):
    def advance_research(self):
        technology = self.technologies[self.research_choice]
        technology.current += self.research
        if technology.current >= technology.required:  # You save left over research
            self.research = technology.current - technology.required
            technology.completed = True
            available_technologies = self.get_available_techs()
            if available_technologies:
                self.research_choice = available_technologies[0].name
            else:
                self.research = 0
        else:
            self.research = 0

    cls.advance_research = advance_research


def establish_requirements_init_addon(county_cls, tech_cls, metadata):
    """Decorate county creation with requirement generation.

    :param county_cls: County object.
    :param tech_cls: Technology object.
    :param metadata: a dictionary of tech requirement names.
    :return: None

    Does:
        metadata = {
            'public works': [
                'engineering',
                'logistics'
            ],
        }
        county = County()
        Technology.establish_requirements(county.technologies, metadata)
    """
    def establish_requirements(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0]  # I think?
            result = func(*args, **kwargs)
            tech_cls.establish_requirements(self.technologies, metadata)
            return result
        return wrapper

    county_cls.__init__ = establish_requirements(county_cls.__init__)
