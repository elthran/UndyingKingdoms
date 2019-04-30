from copy import deepcopy

from undyingkingdoms.models.technologies import Technology

generic_technology = [
    Technology(
        name='Agriculture',
        cost=500,
        tier=1,
        max_level=1,
        description='+50% bonus to all grain production within your county.',
    ),
    Technology(
        name='Animal Husbandry',
        cost=500,
        tier=1,
        max_level=1,
        description='+50% bonus to all dairy production within your county.'),
    Technology(
        name='Steel',
        cost=1000,
        tier=2,
        max_level=1,
        description='+10% Attack Power bonus to all offensive invasions you perform.'),
    Technology(
        name='Engineering',
        cost=250,
        tier=1,
        max_level=1,
        description='+1 building can be built each day.'),
    Technology(
        name='Logistics',
        cost=500,
        tier=1,
        max_level=1,
        description='Your armies return from battle one day sooner.'),
    Technology(
        name='Public Works',
        cost=1000,
        tier=2,
        max_level=1,
        description='Your county generates an additional 1 happiness each day.'),
    Technology(
        name='Arcane Knowledge',
        cost=500,
        tier=1,
        max_level=3,
        description='Each level raises your maximum mana by 20.'),
]

generic_technology = {
    tech.name: tech
    for tech in generic_technology
}

# randomly generated by fake.requirements() as an example
generic_requirements = {
    'agriculture III': ['public works III'],
    'agriculture IV': ['logistics IV', 'engineering IV'],
    'animal husbandry I': ['logistics I'],
    'animal husbandry II': ['logistics II'],
    'animal husbandry III': ['logistics III'],
    'arcane knowledge I': ['logistics I', 'engineering I'],
    'engineering I': ['logistics I'],
    'engineering II': ['steel II'],
    'engineering IV': ['public works IV'],
    'logistics I': ['animal husbandry I'],
    'logistics II': ['agriculture II'],
    'logistics III': ['animal husbandry III', 'public works III'],
    'logistics IV': ['engineering IV', 'arcane knowledge IV'],
    'logistics V': ['public works V', 'steel V'],
    'public works': ['arcane knowledge'],
    'public works III': ['agriculture III', 'logistics III'],
    'public works IV': ['animal husbandry IV'],
    'public works V': ['logistics V'],
    'steel': ['engineering'],
    'steel II': ['animal husbandry II', 'logistics II'],
    'steel III': ['public works III', 'animal husbandry III']
}
