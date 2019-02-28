from undyingkingdoms.models.technologies import Technology

dwarf_technology = {'dwarven muskets': Technology(name='dwarven muskets',
                                                  required=750,
                                                  tier=2,
                                                  max_level=1,
                                                  description='Riflemen get +1 to their defence rating.'),
                    'smelting': Technology(name='smelting',
                                           required=750,
                                           tier=2,
                                           max_level=1,
                                           description='Your iron mines produce 1 additional iron ore each day.')
                    }
