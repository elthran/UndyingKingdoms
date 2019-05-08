from undyingkingdoms.models.technologies import Technology

cleric_technology = {
    Technology(
        name='Blessings',
        cost=750,
        max_level=3,
        description='Grant +1 health to all units.'
    ),
}

cleric_technology = {
    tech.key: tech
    for tech in cleric_technology
}
