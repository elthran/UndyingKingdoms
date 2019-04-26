from copy import deepcopy

from undyingkingdoms.models.technologies import Technology

generic_technology = {
    'agriculture': Technology(
        name='agriculture',
        required=500,
        tier=1,
        max_level=1,
        description='+50% bonus to all grain production within your county.',
    ),
    'animal husbandry': Technology(
        name='animal husbandry',
        required=500,
        tier=1,
        max_level=1,
        description='+50% bonus to all dairy production within your county.'),
    'steel': Technology(
        name='steel',
        required=1000,
        tier=2,
        max_level=1,
        description='+10% Attack Power bonus to all offensive invasions you perform.'),
    'engineering': Technology(
        name='engineering',
        required=250,
        tier=1,
        max_level=1,
        description='+1 building can be built each day.'),
    'logistics': Technology(
        name='logistics',
        required=500,
        tier=1,
        max_level=1,
        description='Your armies return from battle one day sooner.'),
    'public works': Technology(
        name='public works',
        required=1000,
        tier=2,
        max_level=1,
        description='Your county generates an additional 1 happiness each day.'),
    'arcane knowledge I': Technology(
        name='arcane knowledge I',
        required=500,
        tier=1,
        max_level=3,
        description='Each level raises your maximum mana by 20.'),
    'arcane knowledge II': Technology(
        name='arcane knowledge II',
        required=500,
        tier=2,
        max_level=3,
        description='Each level raises your maximum mana by 20.'),
    'arcane knowledge III': Technology(
        name='arcane knowledge III',
        required=500,
        tier=3,
        max_level=3,
        description='Each level raises your maximum mana by 20.')
}

generic_requirements = {
    'public works': [
        'engineering',
        'logistics'
    ],
}

