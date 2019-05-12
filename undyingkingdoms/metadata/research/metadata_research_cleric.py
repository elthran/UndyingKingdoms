from undyingkingdoms.models.effects import Add
from undyingkingdoms.models.technologies import Technology

cleric_technology = {
    Technology(
        name='Blessings',
        cost=750,
        max_level=3,
        description='Grant +{unit_health} health to all units.',
        effects=Add("military", unit_health=1)
    ),
}

cleric_technology = {
    tech.key: tech
    for tech in cleric_technology
}
