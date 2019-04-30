from undyingkingdoms.models.technologies import Technology

rogue_technology = {
    Technology(
        name='Espionage',
        cost=500,
        tier=1,
        max_level=1,
        description='Each thieves den grants an additional thief.'
    ),
}

rogue_technology = {
    tech.key: tech
    for tech in rogue_technology
}
