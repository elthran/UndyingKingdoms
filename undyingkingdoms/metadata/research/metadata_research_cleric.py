from undyingkingdoms.models.effects import Add
from undyingkingdoms.models.technologies import Technology

cleric_technology = {
    Technology(
        name='Missionaries',
        cost=750,
        max_level=1,
        description='Your county has {immigration_modifier:+0.0%} immigration rate.',
        effects=Add('economy', immigration_modifier=0.2),
        source="Cleric"
    ),
    Technology(
        name="Heaven's Blessing",
        cost=1250,
        max_level=1,
        description='Grant +{unit_health} health to all infantry and cavalry units.',
        effects=Add("military", unit_health=1),
        source="Cleric"
    )
}

# it must be a list or it will fail
custom_requirements = {
    "missionaries": ["philosophy iii"],
    "heaven's blessing": ["missionaries"]
}

cleric_technology = {
    tech.key: tech
    for tech in cleric_technology
}
