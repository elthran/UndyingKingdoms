from undyingkingdoms.models.technologies import Technology

warlord_technology = [
    Technology(
        name='Tactician',
        cost=1250,
        max_level=3,
        description='All units gain +1 attack.'
    ),
]

warlord_technology = {
    tech.key: tech
    for tech in warlord_technology
}
