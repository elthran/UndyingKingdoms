from undyingkingdoms.models.effects import Add
from undyingkingdoms.models.technologies import Technology
from undyingkingdoms.models.technologies.helpers import generate_tech_levels

hierophant_technology = {
    Technology(
        name='Unholy Sacrifice',
        cost=500,
        max_level=1,
        description='All infantry and cavalry units gain +1 attack at the cost of -1 to their health.',
        effects=Add('Military', non_monster_non_siege_health=-1, non_monster_non_siege_attack=1),
        source="Hierophant"
    ),
    Technology(
        name='Wall of Bodies',
        cost=500,
        max_level=1,
        description='All infantry and cavalry gain +1 defence at the cost of -1 to their health.',
        effects=Add('Military', non_monster_non_siege_health=-1, non_monster_non_siege_defence=1),
        source="Hierophant"
    )
}


# it must be a list or set it will fail
custom_requirements = {
}

hierophant_technology, hierophant_requirements = generate_tech_levels(hierophant_technology, custom_requirements)
