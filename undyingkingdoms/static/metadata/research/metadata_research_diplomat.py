from undyingkingdoms.models.technologies import Technology

diplomat_technology = {
    Technology(
        name='Diplomacy',
        cost=500,
        tier=1,
        max_level=1,
        description='Each thieves den grants an additional thief.'
    ),
}

diplomat_technology = {
    tech.name: tech
    for tech in diplomat_technology
}
