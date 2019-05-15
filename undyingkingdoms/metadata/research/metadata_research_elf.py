from undyingkingdoms.models.effects import Add
from undyingkingdoms.models.technologies import Technology

elf_technology = {
    Technology(
        name='Knowledge of the Ancients',
        cost=300,
        max_level=1,
        description='Each laboratory generates {research_multiplier} additional research point per day.',
        effects=Add(research_multiplier=1),
        source="Elf"
    ),
    Technology(
        name='Ranger Training',
        cost=1000,
        max_level=1,
        description='Your rangers have {soldier_attack:+} attack.',
        source="Elf",
        effects=Add('military', soldier_attack=1)
    ),
    Technology(
        name='Mithril Armour',
        cost=1500,
        max_level=1,
        description='All non-monster and non-siege units get an additional {non_monster_non_siege_health:+} health point.',
        source="Elf",
        effects=Add('military', non_monster_non_siege_health=1)
    ),
    Technology(
        name='Dragon-fire',
        cost=1000,
        max_level=1,
        description='Dragonhelms have {elite_attack:+} attack.',
        source="Elf",
        effects=Add('military', elite_attack=3)
    )
}

elf_technology = {
    tech.key: tech
    for tech in elf_technology
}
