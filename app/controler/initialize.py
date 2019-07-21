from importlib import import_module
from random import choice

get_specifics = lambda: import_module('app.models.counties.specifics')
get_models = lambda: import_module('app.models.exports')


def initialize_county(user, kingdom, county_name, title, leader_name, race, background):
    """Create a new county object with appropriate preferences and tech."""

    specifics = get_specifics()
    models = get_models()
    county = models.County(
        kingdom.id, county_name, leader_name, user, race, title, background
    )
    models.Preferences(county, user)
    all_requirements = specifics.merge_tech_requirements(county.race, county.background)
    models.Technology.establish_requirements(county.technologies, all_requirements)
    county.research_choice = choice(list(county.available_technologies))
    return county


def pick_kingdom(user, has_clan):
    models = get_models()
    kingdoms = models.Kingdom.query.filter_by(clan=False).all()  # Select all public kingdoms
    smallest_kingdom = min(kingdoms, key=lambda x: len(x.counties))  # Get the smallest
    kingdom = smallest_kingdom
    if has_clan:
        kingdom = user.clan.kingdom
    return kingdom
