from undyingkingdoms.models.effects import Plequals
from undyingkingdoms.models.technologies import Technology

dwarf_technology = {
    Technology(
        name='Dwarven Muskets',
        cost=750,
        max_level=1,
        description='Riflemen get +1 defence.'
    ),
    Technology(
        name='Throwing Axes',
        cost=750,
        max_level=1,
        description='Axemen get +2 defence.'
    ),
    Technology(
        name='Mithril Armour',
        cost=1000,
        max_level=1,
        description='All non-monster and non-siege units get an additional 1 health point.'
    ),
    Technology(
        name='Smelting',
        cost=750,
        max_level=1,
        description='Your iron mines produce {iron_multiplier} additional iron ore each day.',
        effects=Plequals(iron_multiplier=1),
    )
}

dwarf_technology = {
    tech.key: tech
    for tech in dwarf_technology
}
