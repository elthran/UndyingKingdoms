from app.models.effects import Add
from app.models.technologies import Technology
from app.models.technologies.helpers import generate_tech_levels

rogue_technology = {
    Technology(
        name='Advanced Espionage',
        cost=500,
        max_level=3,
        description='All thief missions are {gain_modifier:+0.0%} more effective.',
        effects=Add('Espionage', gain_modifier=0.2),
        source="Rogue"
    ),
    Technology(
        name='Spy Network',
        cost=500,
        max_level=3,
        description='Your thieves return from all missions 10% more quickly.',
        effects=Add('Espionage', duration_multiplier=-0.1),
        source="Rogue"
    )
}

# it must be a list or it will fail
custom_requirements = {
    "advanced espionage": ["basic espionage v"],
    "trade routes": ["advanced espionage iii"]
}

rogue_technology, rogue_requirements = generate_tech_levels(rogue_technology, custom_requirements)
