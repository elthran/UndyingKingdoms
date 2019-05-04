from undyingkingdoms.models.technologies import Technology

alchemist_technology = {
    Technology(
        name='Alchemy',
        cost=500,
        max_level=1,
        description='Each thieves den grants an additional thief.'
    ),
}

alchemist_technology = {
    tech.key: tech
    for tech in alchemist_technology
}
