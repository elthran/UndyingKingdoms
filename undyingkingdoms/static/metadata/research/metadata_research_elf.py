from undyingkingdoms.models.technologies import Technology

elf_technology = {
    Technology(
        name='Knowledge of the Ancients',
        cost=300,
        tier=1,
        max_level=1,
        description='Each laboratory generates one additional research point per day.'
    ),
    Technology(
        name='Ranger Training',
        cost=1000,
        tier=2,
        max_level=1,
        description='Your rangers have +1 attack.'
    ),
    Technology(
        name='Mithril Armour',
        cost=1500,
        tier=3,
        max_level=1,
        description='All non-monster and non-siege units get an additional 1 health point.'
    ),
    Technology(
        name='Dragon-fire',
        cost=1000,
        tier=2,
        max_level=1,
        description='Dragonhelms have +3 attack.'
    )
}

elf_technology = {
    tech.key: tech
    for tech in elf_technology
}
