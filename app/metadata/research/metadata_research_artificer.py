from app.models.effects import Add
from app.models.technologies import Technology
from app.models.technologies.helpers import generate_tech_levels

artificer_technology = {
    Technology(
        name='Advanced Engineering',
        cost=500,
        max_level=3,
        description="All buildings are {cost_modifier:0.0%} cheaper.",
        effects=Add('Infrastructure', cost_modifier=0.1),
        source="Artificer",
    ),
    Technology(
        name='Masonry',
        cost=1000,
        max_level=1,
        description="Your forts are {fort_multiplier:+0.0%} more effective",
        effects=Add('Infrastructure', fort_multiplier=2.0),
        source="Artificer",
    )
}

# it must be a list or it will fail
custom_requirements = {
    "advanced engineering": ["basic engineering v"],
    "masonry": ["advanced engineering iii"]
}

artificer_technology, artificer_requirements = generate_tech_levels(artificer_technology, custom_requirements)
