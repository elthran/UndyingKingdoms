from app.models.effects import Add
from app.models.technologies import Technology
from app.models.technologies.helpers import generate_tech_levels

cleric_technology = {
    Technology(
        name='Missionaries',
        cost=750,
        max_level=1,
        description='Your county has {immigration_modifier:+0.0%} immigration rate.',
        effects=Add('Economy', immigration_modifier=0.2),
        source="Cleric"
    ),
    Technology(
        name="Heaven's Blessing",
        cost=1250,
        max_level=1,
        description='Grant +{unit_health} health to all infantry and cavalry units.',
        effects=Add("Military", unit_health=1),
        source="Cleric"
    )
}

# it must be a list or it will fail
custom_requirements = {
    "missionaries": ["philosophy iii"],
    "heaven's blessing": ["missionaries"]
}

cleric_technology, cleric_requirements = generate_tech_levels(cleric_technology, custom_requirements)
