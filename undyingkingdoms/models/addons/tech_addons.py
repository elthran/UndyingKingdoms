import functools

from extensions import flask_db as db


def completed_techs_addon(cls):
    cls.completed_techs = db.relationship(
        'Technology',
        primaryjoin=(
            "and_("
            "County.id==technology.c.county_id, "
            "technology.c.completed==True"
            ")"
        )

    )


def incomplete_techs_addon(cls):
    cls.incomplete_techs = db.relationship(
        'Technology',
        primaryjoin=(
            "and_("
            "County.id==technology.c.county_id, "
            "technology.c.completed==False"
            ")"
        )

    )


def available_techs_addon(cls):
    def get_available_techs(self):
        completed_tech = self.completed_techs
        available_techs = []
        for tech in self.incomplete_techs:
            if (tech.requirements - completed_tech) is None:
                available_techs.append(tech)
        return available_techs

    cls.get_available_techs = get_available_techs


def advance_research_addon(cls):
    def advance_research(self):
        technology = self.technologies[self.research_choice]
        technology.current += self.research
        if technology.current >= technology.required:  # You save left over research
            self.research = technology.current - technology.required
            technology.completed = True
            available_technologies = self.get_available_technologies()
            if available_technologies:
                self.research_choice = available_technologies[0].name
            else:
                self.research = 0
        else:
            self.research = 0

    cls.advance_research = advance_research


def establish_requirements_init_addon(county_cls, tech_cls, metadata):
    def establish_requirements(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0]  # I think?
            result = func(*args, **kwargs)
            tech_cls.establish_requirements(self.technologies, metadata)
            return result
        return wrapper

    county_cls.__init__ = establish_requirements(county_cls.__init__)
