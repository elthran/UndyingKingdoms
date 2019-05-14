from undyingkingdoms.models.effects import Add
from undyingkingdoms.models.technologies import Technology

artificer_technology = {
    Technology(
        name='Advanced Engineering',
        cost=500,
        max_level=3,
        description="All buildings are {cost_modifier:0.0%} cheaper.",
        effects=Add('infrastructure', cost_modifier=0.1),
        source="Artificer",
    ),
    Technology(
        name='Masonry',
        cost=1000,
        max_level=1,
        description="Your forts are {fort_multiplier:+0.0%} more effective",
        effects=Add('infrastructure', fort_multiplier=2.0),
        source="Artificer",
    )
}

# it must be a list or it will fail
custom_requirements = {
    "advanced engineering": ["basic engineering v"],
    "masonry": ["advanced engineering iii"]
}

artificer_technology = {
    tech.key: tech
    for tech in artificer_technology
}
