from undyingkingdoms.models.effects import Add
from undyingkingdoms.models.technologies import Technology

dwarf_technology = {
    Technology(
        name='Dwarven Muskets',
        cost=1000,
        max_level=1,
        description='Riflemen get {archer_defence:+} defence.',
        source="Dwarf",
        effects=Add('military', archer_defence=1)
    ),
    Technology(
        name='Throwing Axes',
        cost=750,
        max_level=1,
        description='Axemen get +2 defence.',
        source="Dwarf"
    ),
    Technology(
        name='Mithril Armour',
        cost=1500,
        max_level=1,
        description='All non-monster and non-siege units get an additional 2 health point.',
        source="Dwarf"
    ),
    Technology(
        name='Hellfire Cannons',
        cost=2000,
        max_level=1,
        description='Cannons have +5 attack.',
        source="Dwarf"
    ),
    Technology(
        name='Smelting',
        cost=250,
        max_level=1,
        description='Your iron mines produce {iron_multiplier} additional iron ore each day.',
        effects=Add(iron_multiplier=0.5),
        source="Dwarf"
    ),
    Technology(
        name='Battle hardened',
        cost=250,
        max_level=1,
        description='{offensive_modifier:+0.0%} Attack Power bonus to all offensive invasions you perform.',
        effects=Add(offensive_modifier=0.05),
        source="Dwarf"
    )
}

dwarf_technology = {
    tech.key: tech
    for tech in dwarf_technology
}
