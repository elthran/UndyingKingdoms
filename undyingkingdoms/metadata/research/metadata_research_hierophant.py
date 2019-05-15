from undyingkingdoms.models.effects import Add
from undyingkingdoms.models.technologies import Technology
from undyingkingdoms.models.technologies.helpers import generate_tech_levels

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

hierophant_technology, hierophant_requirements = generate_tech_levels(hierophant_technology, custom_requirements)
