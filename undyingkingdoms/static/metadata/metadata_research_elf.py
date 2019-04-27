from undyingkingdoms.models.technologies import Technology

elf_technology = {
    'arcane knowledge': Technology(name='arcane knowledge',
                                   cost=300,
                                   tier=1,
                                   max_level=1,
                                   description='Each laboratory generates one additional research point per day.'),
    'ranger training': Technology(name='ranger training',
                                  cost=1000,
                                  tier=2,
                                  max_level=1,
                                  description='Your rangers have +1 attack.'),
    'mithril armour': Technology(name='mithril armour',
                                 cost=1500,
                                 tier=3,
                                 max_level=1,
                                 description='All non-monster and non-siege units get an additional 1 health point.'),
    'dragon-fire': Technology(name='dragon-fire',
                              cost=1000,
                              tier=2,
                              max_level=1,
                              description='Dragonhelms have +3 attack.')
}
