from undyingkingdoms.models.effects import Times
from undyingkingdoms.models.technologies import Technology

merchant_technology = {
    Technology(
        name='Advanced Economics',
        cost=500,
        max_level=3,
        description='Increases all gold income by {gold_modifier:+0.0%}.',
        effects=Times('economy', gold_modifier=0.1),
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

merchant_technology = {
    tech.key: tech
    for tech in merchant_technology
}
