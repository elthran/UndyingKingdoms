from undyingkingdoms.models.effects import Add
from undyingkingdoms.models.technologies import Technology

alchemist_technology = {
    Technology(
        name='Advanced Alchemy',
        cost=500,
        max_level=3,
        description='Generate an additional +{research_change} research each day.',
        effects=Add(research_change=30),
        source="Alchemist"
    ),
    Technology(
        name='Elixir of Life',
        cost=1000,
        max_level=1,
        description='All non-siege units have +2 health',
        effects=None,
        source="Alchemist"
    )
}

# it must be a list or it will fail
custom_requirements = {
    "advanced alchemy": ["basic alchemy v"],
    "elixir of life": ["advanced alchemy iii"]
}

alchemist_technology = {
    tech.key: tech
    for tech in alchemist_technology
}
