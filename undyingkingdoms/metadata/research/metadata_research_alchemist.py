from undyingkingdoms.models.effects import Plequals
from undyingkingdoms.models.technologies import Technology

alchemist_technology = {
    Technology(
        name='Alchemy',
        cost=500,
        max_level=3,
        description='Generate an additional +{research_change} research each day.',
        effects=Plequals(research_change=5)
    ),
}

alchemist_technology = {
    tech.key: tech
    for tech in alchemist_technology
}
