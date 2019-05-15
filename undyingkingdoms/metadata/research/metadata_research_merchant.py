from undyingkingdoms.models.effects import Add
from undyingkingdoms.models.technologies import Technology
from undyingkingdoms.models.technologies.helpers import generate_tech_levels

merchant_technology = {
    Technology(
        name='Advanced Economics',
        cost=500,
        max_level=3,
        description='Increases all gold income by {gold_modifier:+0.0%}.',
        effects=Add('economy', gold_modifier=0.1),
        source="Merchant"
    ),
    Technology(
        name='Trade Routes',
        cost=1250,
        max_level=1,
        description='Can trade with travelling merchants any resource 1:1.',
        effects=None,
        source="Merchant"
    )
}


# it must be a list or it will fail
custom_requirements = {
    "advanced economics": ["basic economics v"],
    "trade routes": ["advanced economics iii"]
}

merchant_technology, merchant_requirements = generate_tech_levels(merchant_technology, custom_requirements)
