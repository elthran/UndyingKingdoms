from undyingkingdoms.models.technologies import Technology

goblin_technology = {
    Technology(
        name='Slavery',
        cost=1000,
        tier=2,
        max_level=1,
        description='Your slaves are 5 gold, 1 wood, and 1 iron cheaper.'
    ),
    Technology(
        name='Deathwish',
        cost=1000,
        tier=2,
        max_level=1,
        description='Your berserkers have +1 attack.'
    ),
    Technology(
        name='Barbed Arrows',
        cost=1000,
        tier=2,
        max_level=1,
        description='Your bowmen get +1 defence.'
    ),
    Technology(
        name='Cross-breeding',
        cost=1000,
        tier=2,
        max_level=1,
        description='Wolf riders get +3 attack.'
    )
}


goblin_technology = {
    tech.name: tech
    for tech in goblin_technology
}
