from undyingkingdoms.models.effects import Times
from undyingkingdoms.models.technologies import Technology

diplomat_technology = {
    Technology(
        name='Bartering',
        cost=500,
        max_level=1,
        description='Increases all gold income by {gold_modifier:+0.0%}.',
        effects=Times('economy', gold_modifier=0.15),
    ),
}

diplomat_technology = {
    tech.key: tech
    for tech in diplomat_technology
}
