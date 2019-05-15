from undyingkingdoms.models.effects import Add
from undyingkingdoms.models.technologies import Technology

rogue_technology = {
    Technology(
        name='Advanced Espionage',
        cost=500,
        max_level=3,
        description='All thief missions are {gain_modifer:+0.0%} more effective.',
        effects=Add('espionage', gain_modifer=0.2),
        source="Rogue"
    ),
    Technology(
        name='Spy Network',
        cost=500,
        max_level=3,
        description='When your thieves are captured, you can retrain new oes twice as quickly.',
        effects=Add('espionage', duration_multiplier=0.5),
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
