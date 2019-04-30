from undyingkingdoms.models.technologies import Technology

warlord_technology = [
    Technology(
        name='Tactician',
        cost=500,
        tier=1,
        max_level=1,
        description='Each thieves den grants an additional thief.'
    ),
]

warlord_technology = {
    tech.name: tech
    for tech in warlord_technology
}
