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

# it must be a list or it will fail
custom_requirements = {
    "advanced espionage": ["basic espionage v"],
    "trade routes": ["advanced espionage iii"]
}

rogue_technology = {
    tech.key: tech
    for tech in rogue_technology
}
