from undyingkingdoms.models import County, Preferences, Kingdom


def initialize_county(user, kingdom, county_name, leader_name, background, race, title):
    county = County(
        kingdom.id, county_name, leader_name, user.id, race, title, background
    )
    county.save()
    county.vote = county.id
    preferences = Preferences(county.id, user.id)
    preferences.save()
    return county


def pick_kingdom(user, has_clan):
    kingdoms = Kingdom.query.filter_by(clan=False).all()  # Select all public kingdoms
    smallest_kingdom = min(kingdoms, key=lambda x: len(x.counties))  # Get the smallest
    kingdom = smallest_kingdom
    if has_clan:
        kingdom = user.clan.kingdom
    return kingdom
