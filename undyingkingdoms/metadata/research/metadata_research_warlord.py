from undyingkingdoms.models.effects import Add
from undyingkingdoms.models.technologies import Technology

warlord_technology = {
    Technology(
        name='Advanced Logistics',
        cost=500,
        max_level=1,
        description='Your armies return from battle {speed} days sooner.',
        effects=Add(speed=1),
        source="Warlord"
    ),
    Technology(
        name='Battle Tactics',
        cost=1000,
        max_level=1,
        description='{offensive_modifier:+0.0%} Attack Power bonus to all offensive invasions you perform.',
        effects=Add('military', offensive_modifier=0.15),
        source="Warlord"
    )
}


# it must be a list or it will fail
custom_requirements = {
    "advanced logistics": ["basic logistics iii"],
    "trade routes": ["advanced logistics"]
}

warlord_technology = {
    tech.key: tech
    for tech in warlord_technology
}
