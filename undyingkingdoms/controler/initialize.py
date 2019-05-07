from random import choice

from undyingkingdoms.metadata.research.metadata_research_all import generic_requirements
from undyingkingdoms.models.exports import County, Preferences, Kingdom, Technology


def initialize_county(user, kingdom, county_name, title, leader_name, race, background):
    """Create a new county object with appropriate preferences and tech."""
    county = County(
        kingdom.id, county_name, leader_name, user, race, title, background
    )
    Preferences(county, user)
    # requirements = fake.requirements(county.technologies.keys())
    Technology.establish_requirements(county.technologies, generic_requirements)
    county.research_choice = choice(list(county.available_techs))
    return county


def pick_kingdom(user, has_clan):
    kingdoms = Kingdom.query.filter_by(clan=False).all()  # Select all public kingdoms
    smallest_kingdom = min(kingdoms, key=lambda x: len(x.counties))  # Get the smallest
    kingdom = smallest_kingdom
    if has_clan:
        kingdom = user.clan.kingdom
    return kingdom
