from undyingkingdoms.models.effects import Add
from undyingkingdoms.models.technologies import Technology

hierophant_technology = {
    Technology(
        name='Sacrifice',
        cost=5,
        max_level=1,
        description='...',
        effects=Add('military', unit_health=-1, unit_attack=2),
        source="Hierophant"
    ),
    Technology(
        name='Sacrifice 2',
        cost=5,
        max_level=1,
        description='...',
        effects=Add('military', unit_health=-2, unit_attack=3),
        source="Hierophant"
    )
}


# it must be a list or set it will fail
custom_requirements = {
}

hierophant_technology = {
    tech.key: tech
    for tech in hierophant_technology
}
