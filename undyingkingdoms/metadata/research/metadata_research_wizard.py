from undyingkingdoms.models.effects import Add
from undyingkingdoms.models.technologies import Technology

wizard_technology = [
    Technology(
        name='Advanced Channelling',
        cost=500,
        max_level=1,
        description='Generate an additional mana each day.',
        effects=Add(mana_change=1),
        source="Wizard"
    ),
    Technology(
        name='Hellcaster',
        cost=500,
        max_level=1,
        description='When your spells are disrupted, you are able to recover half of the spent mana.',
        effects=None,
        source="Wizard"
    )
]


# it must be a list or it will fail
custom_requirements = {
    "advanced channelling": ["basic channelling v"],
    "nature's blessing": ["advanced channelling iii"]
}

wizard_technology = {
    tech.key: tech
    for tech in wizard_technology
}
