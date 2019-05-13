from undyingkingdoms.models.effects import Add
from undyingkingdoms.models.technologies import Technology

alchemist_technology = {
    Technology(
        name='Advanced Alchemy',
        cost=500,
        max_level=3,
        description='Generate an additional +{research_change} research each day.',
        effects=Add('scientist', research_change=30),
        source="Alchemist"
    ),
    Technology(
        name='Elixir of Life',
        cost=1000,
        max_level=1,
        description='All non-siege units have +{non_siege_health} health',
        effects=Add('military', non_siege_health=2),
        source="Alchemist"
    )
}

# it must be a list or it will fail
custom_requirements = {
    "advanced alchemy": ["basic alchemy v"],
}

alchemist_technology = {
    tech.key: tech
    for tech in alchemist_technology
}
