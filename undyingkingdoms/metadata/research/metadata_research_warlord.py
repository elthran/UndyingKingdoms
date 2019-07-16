from undyingkingdoms.models.effects import Add, Times
from undyingkingdoms.models.technologies import Technology
from undyingkingdoms.models.technologies.helpers import generate_tech_levels

warlord_technology = {
    Technology(
        name='Advanced Logistics',
        cost=500,
        max_level=1,
        description='Your armies return from battle {speed} days sooner.',
        effects=Add('Military', speed=1),
        source="Warlord"
    ),
    Technology(
        name='Battle Tactics',
        cost=1000,
        max_level=1,
        description='{offensive_modifier:+0.0%} Attack Power bonus to all offensive invasions you perform.',
        effects=Add('Military', offensive_modifier=0.15),
        source="Warlord"
    ),
    Technology(
        name="Call to Arms",
        description="You can train {trainable_per_day_modifier:+0.0%} more soldiers per day",
        cost=1250,
        max_level=1,
        source="Warlord",
        effects=Add('Military', trainable_per_day_modifier=0.2)
    )
}


# it must be a list or it will fail
custom_requirements = {
    "advanced logistics": ["basic logistics iii"],
    "trade routes": ["advanced logistics"],
    "call to arms": ["battle tactics"],
}

warlord_technology, warlord_requirements = generate_tech_levels(warlord_technology, custom_requirements)


