from undyingkingdoms.models.effects import Add
from undyingkingdoms.models.technologies import Technology

artificer_technology = {
    Technology(
        name='Advanced Engineering',
        cost=500,
        max_level=3,
        description="All buildings are 10% cheaper.",
        output=0.10,
        effects=None,
        source="Artificer"
    ),
    Technology(
        name='Masonry',
        cost=1000,
        max_level=1,
        description="You generate +{stone_produced} additional stone each day per quarry.",
        output=5,
        effects=Add(stone_produced=1),
        source="Artificer"
    ),
}

artificer_technology = {
    tech.key: tech
    for tech in artificer_technology
}
