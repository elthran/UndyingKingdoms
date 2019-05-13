from undyingkingdoms.models.technologies import Technology

rogue_technology = {
    Technology(
        name='Advanced Espionage',
        cost=500,
        max_level=3,
        description='All thief missions are +20% more effective.',
        effects=None,
        source="Rogue"
    ),
    Technology(
        name='Spy Network',
        cost=500,
        max_level=3,
        description='When your thieves are captured, you can retrain new oes twice as quickly.',
        effects=None,
        source="Rogue"
    )
}

rogue_technology = {
    tech.key: tech
    for tech in rogue_technology
}
