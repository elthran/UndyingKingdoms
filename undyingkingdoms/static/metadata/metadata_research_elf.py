from undyingkingdoms.models.technologies import Technology

elf_technology = {'arcane knowledge': Technology(name='arcane knowledge',
                                                 required=300,
                                                 tier=1,
                                                 max_level=1,
                                                 description='Each laboratory generates one additional research point per day.'),
                  'mithril armour': Technology(name='mithril armour',
                                               required=1500,
                                               tier=3,
                                               max_level=1,
                                               description='All non-monster units get an additional 1 health point..')
                  }
