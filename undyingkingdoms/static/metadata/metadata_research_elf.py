from undyingkingdoms.models.technologies import Technology

elf_technology = {
    'arcane knowledge': Technology(name='arcane knowledge',
                                   required=300,
                                   tier=1,
                                   max_level=1,
                                   description='Each laboratory generates one additional research point per day.'),
    'ranger training': Technology(name='ranger training',
                                  required=1000,
                                  tier=2,
                                  max_level=1,
                                  description='Your rangers have +1 attack.'),
    'mithril armour': Technology(name='mithril armour',
                                 required=1500,
                                 tier=3,
                                 max_level=1,
                                 description='All non-monster and non-siege units get an additional 1 health point.'),
    'ranger training': Technology(name='ranger training',
                                  required=1000,
                                  tier=2,
                                  max_level=1,
                                  description='Your rangers have +1 attack.'),
    'dragon-fire': Technology(name='dragon-fire',
                              required=1000,
                              tier=2,
                              max_level=1,
                              description='Dragonhelms have +3 attack.')
}
