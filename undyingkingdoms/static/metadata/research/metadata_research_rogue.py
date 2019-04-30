from undyingkingdoms.models.technologies import Technology

rogue_technology = {
    Technology(
        name='espionage i',
        cost=500,
        tier=1,
        max_level=1,
        description='Each thieves den grants an additional thief.'
    ),
}

rogue_technology = {
    tech.name: tech
    for tech in rogue_technology
}
