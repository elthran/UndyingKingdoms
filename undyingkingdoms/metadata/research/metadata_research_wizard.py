from undyingkingdoms.models.effects import Add
from undyingkingdoms.models.technologies import Technology
from undyingkingdoms.models.technologies.helpers import generate_tech_levels

wizard_technology = [
    Technology(
        name='Advanced Channelling',
        cost=500,
        max_level=1,
        description='Generate an additional mana each day.',
        effects=Add('wizardry', mana_change=1),
        source="Wizard"
    ),
    Technology(
        name='Hellcaster',
        cost=500,
        max_level=1,
        description='When your spells are disrupted, you are able to recover half of the spent mana.',
        effects=Add('wizardry', recoup_factor=0.5),
        source="Wizard"
    )
]


# it must be a list or it will fail
custom_requirements = {
    "advanced channelling": ["basic channelling v"],
    "nature's blessing": ["advanced channelling iii"]
}

wizard_technology, wizard_requirements = generate_tech_levels(wizard_technology, custom_requirements)
