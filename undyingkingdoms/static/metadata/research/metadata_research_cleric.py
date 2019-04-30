from undyingkingdoms.models.technologies import Technology

cleric_technology = {
    Technology(
        name='Blessings',
        cost=500,
        tier=1,
        max_level=1,
        description='Each thieves den grants an additional thief.'
    ),
}

cleric_technology = {
    tech.name: tech
    for tech in cleric_technology
}
