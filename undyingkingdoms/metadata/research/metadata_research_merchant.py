from undyingkingdoms.models.effects import Times
from undyingkingdoms.models.technologies import Technology

merchant_technology = {
    Technology(
        name='Mercantilism',
        cost=750,
        max_level=3,
        description='Increases all gold income by {gold_modifier:+0.0%}.',
        effects=Times('economy', gold_modifier=0.1),
    )
}

merchant_technology = {
    tech.key: tech
    for tech in merchant_technology
}
