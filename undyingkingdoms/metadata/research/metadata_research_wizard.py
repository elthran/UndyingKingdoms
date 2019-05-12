from undyingkingdoms.models.effects import Plequals
from undyingkingdoms.models.technologies import Technology

wizard_technology = [
    Technology(
        name='Spell Crafting',
        cost=500,
        max_level=1,
        description='Generate an additional mana each day.',
        effects=Plequals(mana_change=1)
    )
]

wizard_technology = {
    tech.key: tech
    for tech in wizard_technology
}
