from undyingkingdoms.models.technologies import Technology

dwarf_technology = {
    'dwarven muskets': Technology(name='dwarven muskets',
                                  required=750,
                                  tier=2,
                                  max_level=1,
                                  description='Riflemen get +1 defence.'),
    'throwing axes': Technology(name='throwing axes',
                                required=750,
                                tier=1,
                                max_level=1,
                                description='Axemen get +2 defence.'),
    'mithril armour': Technology(name='mithril armour',
                                 required=1000,
                                 tier=2,
                                 max_level=1,
                                 description='All non-monster and non-siege units get an additional 1 health point.'),
    'smelting': Technology(name='smelting',
                           required=750,
                           tier=2,
                           max_level=1,
                           description='Your iron mines produce 1 additional iron ore each day.')
}
