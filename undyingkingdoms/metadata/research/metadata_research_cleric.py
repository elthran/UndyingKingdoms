from undyingkingdoms.models.effects import Add
from undyingkingdoms.models.technologies import Technology

cleric_technology = {
    Technology(
        name='Missionaries',
        cost=750,
        max_level=1,
        description='Your county has +20% immigration rate.',
        effects=None,
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

cleric_technology = {
    tech.key: tech
    for tech in cleric_technology
}
