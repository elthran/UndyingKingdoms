from undyingkingdoms.models.effects import Times
from undyingkingdoms.models.technologies import Technology

human_technology = {
    Technology(
        name='Civic Duty',
        cost=500,
        max_level=1,
        description='Reduces upkeep cost of men-at-arms by 10 gold each.',
        source="Human"
    ),
    Technology(
        name='Economics',
        cost=750,
        max_level=1,
        description='Increases all gold income by {gold_modifier:+0.0%}.',
        effects=Times('economy', gold_modifier=0.15),
        source="Human"
    ),
    Technology(
        name='Knights Templar',
        cost=1000,
        max_level=1,
        description='All knights get +3 attack.',
        source="Human"
    ),
    Technology(
        name='Trading',
        cost=750,
        max_level=1,
        description='All military units cost 5 less gold to train.',
        source="Human"
    )
}

human_technology = {
    tech.key: tech
    for tech in human_technology
}
