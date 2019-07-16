from undyingkingdoms.models.effects import Add
from undyingkingdoms.models.technologies import Technology
from undyingkingdoms.models.technologies.helpers import generate_tech_levels

alchemist_technology = {
    Technology(
        name='Advanced Alchemy',
        cost=500,
        max_level=3,
        description='Generate an additional +{research_change} research each day.',
        effects=Add('Scientist', research_change=30),
        source="Alchemist"
    ),
    Technology(
        name='Elixir of Life',
        cost=1000,
        max_level=1,
        description='All non-siege units have +{non_siege_health} health',
        effects=Add('Military', non_siege_health=2),
        source="Alchemist"
    )
}

# it must be a list or it will fail
custom_requirements = {
    "advanced alchemy": ["basic alchemy v"],
    "elixir of life": ["advanced alchemy iii"]
}

alchemist_technology, alchemist_requirements = generate_tech_levels(alchemist_technology, custom_requirements)
