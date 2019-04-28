from copy import deepcopy

from undyingkingdoms.models.technologies import Technology

generic_technology = {
    'agriculture': Technology(
        name='agriculture',
        cost=500,
        tier=1,
        max_level=1,
        description='+50% bonus to all grain production within your county.',
    ),
    'animal husbandry': Technology(
        name='animal husbandry',
        cost=500,
        tier=1,
        max_level=1,
        description='+50% bonus to all dairy production within your county.'),
    'steel': Technology(
        name='steel',
        cost=1000,
        tier=2,
        max_level=1,
        description='+10% Attack Power bonus to all offensive invasions you perform.'),
    'engineering': Technology(
        name='engineering',
        cost=250,
        tier=1,
        max_level=1,
        description='+1 building can be built each day.'),
    'logistics': Technology(
        name='logistics',
        cost=500,
        tier=1,
        max_level=1,
        description='Your armies return from battle one day sooner.'),
    'public works': Technology(
        name='public works',
        cost=1000,
        tier=2,
        max_level=1,
        description='Your county generates an additional 1 happiness each day.'),
    'arcane knowledge': Technology(
        name='arcane knowledge',
        cost=500,
        tier=1,
        max_level=3,
        description='Each level raises your maximum mana by 20.'),
    # 'arcane knowledge II': Technology(
    #     name='arcane knowledge II',
    #     cost=500,
    #     tier=2,
    #     max_level=3,
    #     description='Each level raises your maximum mana by 20.'),
    # 'arcane knowledge III': Technology(
    #     name='arcane knowledge III',
    #     cost=500,
    #     tier=3,
    #     max_level=3,
    #     description='Each level raises your maximum mana by 20.')
}

generic_technology = {**{k + " I": v for k, v in generic_technology}}

generic_requirements = {
    'public works': [
        'engineering',
        'logistics'
    ],
}

