from undyingkingdoms.models.technologies import Technology

alchemist_technology = {
    Technology(
        name='Alchemy',
        cost=500,
        max_level=3,
        description='Generate an additional +5 research each day.',
        output=5
    ),
}

alchemist_technology = {
    tech.key: tech
    for tech in alchemist_technology
}
